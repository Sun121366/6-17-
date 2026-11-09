# szj: ===== comments 应用 · 视图层（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 本模块提供两个视图：
# szj:   1) CommentPostView     —— 处理“发表评论 / 回复评论”表单，需登录并带 CSRF 保护；
# szj:   2) CommentReactionView —— 评论 Emoji 反应 JSON API（GET 公开、POST 需登录）。
# szj: 本次质量改进：
# szj:   - 文章关闭评论时由 raise ValidationError（会变成 500）改为返回 403 响应；
# szj:   - comment.save(True) 改为显式的 save(force_insert=True)，消除魔法位置参数；
# szj:   - get_blog_setting 改为模块级导入，parent_comment 查询改为 get_object_or_404；
# szj:   - 合法的 Emoji 类型集合提升为模块级 frozenset，避免每次请求重复构造列表。
"""评论相关视图。

负责把用户在文章详情页提交的评论落库（含审核开关与嵌套回复），
以及为前端提供评论 Emoji 反应的查询与切换接口。
"""

from django.contrib.auth import get_user_model
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views import View

from blog.models import Article
from djangoblog.base_views import AuthenticatedFormView
from djangoblog.utils import get_blog_setting

from .forms import CommentForm
from .models import Comment, CommentReaction

# szj: 从模型 choices 派生合法 Emoji 集合，供 POST 校验使用（不可变、可复用于多次请求）。
VALID_REACTION_TYPES = frozenset(choice[0] for choice in CommentReaction.REACTION_CHOICES)


class CommentPostView(AuthenticatedFormView):
    """评论提交视图。

    继承 AuthenticatedFormView 后自动获得：
    - 登录校验（未登录用户被重定向到登录页）；
    - CSRF 保护（表单提交必须携带 token）。
    """

    form_class = CommentForm
    template_name = 'blog/article_detail.html'

    def get(self, request, *args, **kwargs):
        """GET 请求不做渲染，直接跳回文章详情页的评论区锚点。"""
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        """表单校验失败时，带错误信息与文章上下文重新渲染文章详情页。"""
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])

        return self.render_to_response({
            'form': form,
            'article': article
        })

    def form_valid(self, form):
        """校验通过：组装评论对象并落库，随后跳转到新评论对应的锚点。

        :param form: 已通过校验的 CommentForm
        :return: 指向新评论锚点的 302 重定向响应
        """
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])

        # szj: 业务规则 1：文章自身关闭评论（comment_status='c'）或文章已关闭（status='c'）时禁止评论。
        # szj: 原实现直接 raise ValidationError 会被 Django 当作未处理异常返回 500，这里改为明确的 403。
        if article.comment_status == 'c' or article.status == 'c':
            return HttpResponseForbidden('该文章评论已关闭。')

        # szj: 业务规则 2：用 commit=False 先拿到未保存实例，补齐文章与作者后再统一落库。
        comment = form.save(commit=False)
        comment.article = article
        # szj: 评论作者直接使用当前登录用户（AuthenticatedFormView 已保证已登录）。
        comment.author = get_user_model().objects.get(pk=self.request.user.pk)

        # szj: 业务规则 3：站点开启“评论需要审核”时保持 is_enable=False，否则直接放行展示。
        if not get_blog_setting().comment_need_review:
            comment.is_enable = True

        # szj: 业务规则 4：parent_comment_id 非空表示这是回复，挂到父评论上形成嵌套结构。
        parent_comment_id = form.cleaned_data['parent_comment_id']
        if parent_comment_id:
            comment.parent_comment = get_object_or_404(
                Comment, pk=parent_comment_id)

        # szj: 显式 force_insert=True：语义清晰，也避免 save(True) 位置参数被误读成其他含义。
        comment.save(force_insert=True)
        return HttpResponseRedirect(
            f'{article.get_absolute_url()}#div-comment-{comment.pk}')


class CommentReactionView(View):
    """评论 Emoji 反应 API。

    - ``GET  /comment/<comment_id>/react``：公开查询评论的反应统计；
    - ``POST /comment/<comment_id>/react``：登录用户切换（点赞/取消）某个反应。
    """

    def get(self, request, comment_id):
        """查询指定评论的 reactions 统计（公开访问，未登录用户 has_reacted 恒为 False）。"""
        comment = get_object_or_404(Comment, id=comment_id, is_enable=True)

        # szj: 未登录时传 None，方法内部据此跳过“当前用户是否已点赞”的查询。
        user = request.user if request.user.is_authenticated else None
        reactions_data = comment.get_reactions_summary(user)

        return JsonResponse({
            'success': True,
            'reactions': reactions_data
        })

    def post(self, request, comment_id):
        """切换当前用户对某条评论的某个 Emoji 反应（需登录）。

        :param comment_id: 评论主键
        :return: JSON，action 为 ``added`` 或 ``removed``
        """
        # szj: 权限校验：POST 接口只对已登录用户开放，返回 401 便于前端引导登录。
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        # szj: 只能对“已通过审核、前台可见”的评论点赞，避免越权操作待审核内容。
        comment = get_object_or_404(Comment, id=comment_id, is_enable=True)

        # szj: 参数校验：reaction_type 必须是 REACTION_CHOICES 中定义过的 Emoji。
        reaction_type = request.POST.get('reaction_type')
        if reaction_type not in VALID_REACTION_TYPES:
            return JsonResponse({
                'error': 'Invalid reaction type'
            }, status=400)

        # szj: 切换语义：已存在则删除（取消点赞），不存在则创建（点赞），依赖联合唯一约束保证幂等。
        reaction, created = CommentReaction.objects.get_or_create(
            comment=comment,
            user=request.user,
            reaction_type=reaction_type
        )

        if created:
            action = 'added'
        else:
            reaction.delete()
            action = 'removed'

        # szj: 返回最新统计，前端可直接用返回值刷新按钮上的计数，无需再发一次 GET。
        return JsonResponse({
            'success': True,
            'action': action,
            'reactions': comment.get_reactions_summary(request.user)
        })
