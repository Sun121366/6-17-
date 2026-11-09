# szj: ===== comments 应用 · 模型层（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 本模块定义博客评论系统的两张核心数据表：
# szj:   1) Comment         —— 文章评论，通过自关联 parent_comment 支持无限嵌套回复；
# szj:   2) CommentReaction —— 评论的 Emoji 点赞/反应，靠联合唯一约束防止重复点赞。
# szj: 精读要点：Meta 中的两个组合索引分别服务“文章评论列表”和“侧边栏最新评论”两类高频查询；
# szj: get_reactions_summary 原实现存在 N+1 查询，本次已改为批量查询并在方法内注明。
"""评论与互动模型。

定义文章评论、嵌套回复以及评论的 Emoji 反应关系，用于描述用户围绕文章
产生的互动数据。评论与反应都以文章、用户为外键，文章或用户被删除时级联清理。
"""

# szj: 用 defaultdict 在内存中按 Emoji 类型分组，替代逐类查询（见 get_reactions_summary）。
from collections import defaultdict

from django.conf import settings
from django.db import models
# szj: Count / defaultdict 改为模块级导入，修复 pylint C0415（函数内导入）。
from django.db.models import Count
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from blog.models import Article

# szj: 反应摘要里每种 Emoji 最多展示的用户名数量，与原实现保持一致（原为切片 [:10]）。
MAX_REACTION_USERS = 10


# Create your models here.

class Comment(models.Model):
    # [TWL/唐文龙] 以下模型说明由本人补充。
    """文章评论模型。

    author 指向评论用户，article 指向被评论文章，parent_comment 通过自关联
    实现回复评论；comment.is_enable 控制评论是否通过审核并对外展示。
    """
    # 评论正文，当前最大长度为 300 个字符。 [TWL]
    body = models.TextField('正文', max_length=300)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    # 评论作者：一个用户可以发表多条评论。 [TWL]
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        on_delete=models.CASCADE)
    # 所属文章：一篇文章可以包含多条评论。 [TWL]
    article = models.ForeignKey(
        Article,
        verbose_name=_('article'),
        on_delete=models.CASCADE)
    # 父评论：为空表示顶层评论，非空表示对某条评论的回复。 [TWL]
    parent_comment = models.ForeignKey(
        'self',
        verbose_name=_('parent comment'),
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    is_enable = models.BooleanField(_('enable'),
                                    default=False, blank=False, null=False)

    class Meta:
        """模型元信息：默认按主键倒序，并声明两条高频查询的组合索引。"""

        ordering = ['-id']
        verbose_name = _('comment')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'
        indexes = [
            # 优化评论列表查询：article + parent_comment + is_enable组合索引
            models.Index(
                fields=['article', 'parent_comment', 'is_enable'],
                name='idx_art_parent_enable'),
            # 优化侧边栏评论查询：is_enable + id组合索引
            models.Index(fields=['is_enable', '-id'], name='idx_enable_id'),
        ]

    def __str__(self):
        """后台与调试场景下的可读标识，直接使用评论正文。"""
        return self.body

    def get_reactions_summary(self, user=None):
        """汇总当前评论的 Emoji 反应信息。

        返回结构::

            {
                '👍': {'count': 5, 'has_reacted': True, 'users': ['Alice', 'Bob']},
                '❤️': {'count': 3, 'has_reacted': False, 'users': ['Carol']},
                ...
            }

        :param user: 当前登录用户；未登录或传 None 时 ``has_reacted`` 恒为 False。
        :return: 以 Emoji 字符为键、统计信息为值的字典。
        """
        # szj: 性能改进：原实现为“1 次聚合 + 每种 Emoji 再查 2 次”，共 1 + 2N 次查询；
        # szj: 现拆成 3 次批量查询（计数、用户列表、当前用户已点类型），与 Emoji 种类数无关。
        reaction_counts = (
            CommentReaction.objects.filter(comment=self)
            .values('reaction_type')
            .annotate(count=Count('id'))
        )
        if not reaction_counts:
            return {}

        # szj: 第一步：一次查出该评论的全部反应记录（含用户），在内存里按 Emoji 分组，
        # szj: 每组只保留前 MAX_REACTION_USERS 个用户名，避免为每种 Emoji 单独发起查询。
        users_by_reaction = defaultdict(list)
        reaction_rows = (
            CommentReaction.objects.filter(comment=self)
            .select_related('user')
            .order_by('id')
        )
        for reaction in reaction_rows:
            user_names = users_by_reaction[reaction.reaction_type]
            if len(user_names) < MAX_REACTION_USERS:
                user_names.append(reaction.user.nickname or reaction.user.username)

        # szj: 第二步：已登录用户只需一次查询，即可知道自己在该评论上点过哪些 Emoji。
        reacted_types = set()
        if user is not None and getattr(user, 'is_authenticated', False):
            reacted_types = set(
                CommentReaction.objects.filter(comment=self, user=user)
                .values_list('reaction_type', flat=True)
            )

        # szj: 第三步：把聚合计数与内存分组合并成最终结果，保证前端拿到的结构与旧版一致。
        return {
            item['reaction_type']: {
                'count': item['count'],
                'has_reacted': item['reaction_type'] in reacted_types,
                'users': users_by_reaction.get(item['reaction_type'], []),
            }
            for item in reaction_counts
        }


class CommentReaction(models.Model):
    """评论的 Emoji 反应（点赞）记录。

    同一用户对同一条评论的同一种 Emoji 只能存在一条记录，用于实现
    “点赞 / 取消点赞”的切换语义，并为前端提供各 Emoji 的计数与用户列表。
    """

    # szj: 支持的反应类型与语义名，前端通过 get_reactions_summary 拿到的是 Emoji 字符本身。
    REACTION_CHOICES = [
        ('👍', 'thumbs_up'),
        ('👎', 'thumbs_down'),
        ('❤️', 'heart'),
        ('😄', 'laugh'),
        ('🎉', 'hooray'),
        ('😕', 'confused'),
        ('🚀', 'rocket'),
        ('👀', 'eyes'),
    ]

    # 被反应的评论。 [TWL]
    comment = models.ForeignKey(
        Comment,
        verbose_name=_('comment'),
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    # 发起评论反应的用户。 [TWL]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.CASCADE
    )
    # Emoji 反应类型，同一用户对同一评论的同一类型只能记录一次。 [TWL]
    reaction_type = models.CharField(
        _('reaction type'),
        max_length=10,
        choices=REACTION_CHOICES
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        """模型元信息：联合唯一约束保证幂等，comment + reaction_type 索引服务分组统计。"""

        verbose_name = _('comment reaction')
        verbose_name_plural = _('comment reactions')
        # 数据库唯一约束：防止重复点赞或重复添加同一种 Emoji 反应。 [TWL]
        unique_together = ['comment', 'user', 'reaction_type']
        indexes = [
            models.Index(fields=['comment', 'reaction_type'],
                         name='idx_comment_reaction'),
        ]

    def __str__(self):
        """后台展示用字符串：谁 + 对哪条评论 + 哪种反应。"""
        return (f'{self.user.username} - {self.reaction_type} '
                f'on comment {self.comment.id}')
