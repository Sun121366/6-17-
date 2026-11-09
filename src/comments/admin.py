# szj: ===== comments 应用 · 后台管理（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 本模块把评论与评论反应注册进 Django Admin，并提供：
# szj:   - 评论列表的批量启用/禁用 action；
# szj:   - 评论作者、所属文章、反应目标的可点击跳转列。
# szj: 本次质量改进：补齐模块/类/方法 docstring；format_html 改为参数化插值（自动转义更安全）；
# szj: 去掉 Python 2 遗留的 u'' 前缀与 % 格式化；把重复的 admin 链接拼装抽成 _admin_change_link。
"""评论应用的后台管理配置。

为评论（Comment）与评论反应（CommentReaction）两类模型提供列表展示、
筛选、搜索与批量审核入口，是站点运营人员管理评论的主要界面。
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Comment, CommentReaction


def _admin_change_link(obj):
    """生成指向某个模型实例后台详情页的 admin change 链接。

    :param obj: 任意 Django 模型实例
    :return: 形如 ``/admin/comments/comment/1/change/`` 的 URL 字符串
    """
    info = (obj._meta.app_label, obj._meta.model_name)
    return reverse(f'admin:{info[0]}_{info[1]}_change', args=(obj.id,))


def disable_commentstatus(modeladmin, request, queryset):
    """批量操作：把选中的评论设为“未通过审核/不对外展示”。"""
    del modeladmin, request  # szj: 批量 action 用不到这两个参数，显式丢弃以消除告警。
    queryset.update(is_enable=False)


def enable_commentstatus(modeladmin, request, queryset):
    """批量操作：把选中的评论设为“已通过审核/对外展示”。"""
    del modeladmin, request  # szj: 同上，仅使用 queryset。
    queryset.update(is_enable=True)


disable_commentstatus.short_description = _('Disable comments')
enable_commentstatus.short_description = _('Enable comments')


class CommentAdmin(admin.ModelAdmin):
    """评论后台：列表展示、按审核状态筛选、按正文搜索，并提供可跳转的作者/文章列。"""

    list_per_page = 20
    list_display = (
        'id',
        'body',
        'link_to_userinfo',
        'link_to_article',
        'is_enable',
        'creation_time')
    list_display_links = ('id', 'body', 'is_enable')
    list_filter = ('is_enable',)
    exclude = ('creation_time', 'last_modify_time')
    actions = [disable_commentstatus, enable_commentstatus]
    raw_id_fields = ('author', 'article')
    search_fields = ('body',)

    def link_to_userinfo(self, obj):
        """列表列：把评论作者渲染成指向其后台详情页的链接。"""
        # szj: format_html 会把参数自动做 HTML 转义，比手写 % 拼接更安全。
        return format_html(
            '<a href="{}">{}</a>',
            _admin_change_link(obj.author),
            obj.author.nickname if obj.author.nickname else obj.author.email)

    def link_to_article(self, obj):
        """列表列：把评论所属文章渲染成指向该文章后台详情页的链接。"""
        return format_html(
            '<a href="{}">{}</a>',
            _admin_change_link(obj.article),
            obj.article.title)

    link_to_userinfo.short_description = _('User')
    link_to_article.short_description = _('Article')


class CommentReactionAdmin(admin.ModelAdmin):
    """评论反应后台：按反应类型/时间筛选，支持跳转评论与用户详情。"""

    list_display = ('id', 'reaction_type', 'link_to_comment',
                    'link_to_user', 'created_at')
    list_display_links = ('id', 'reaction_type')
    list_filter = ('reaction_type', 'created_at')
    raw_id_fields = ('comment', 'user')
    search_fields = ('comment__body', 'user__username')
    date_hierarchy = 'created_at'

    def link_to_comment(self, obj):
        """列表列：跳转到该反应对应的评论详情页。"""
        return format_html(
            '<a href="{}">Comment #{}</a>', _admin_change_link(obj.comment),
            obj.comment.id)

    def link_to_user(self, obj):
        """列表列：跳转到发起该反应的用户详情页。"""
        return format_html(
            '<a href="{}">{}</a>',
            _admin_change_link(obj.user),
            obj.user.nickname if obj.user.nickname else obj.user.username)

    link_to_comment.short_description = _('Comment')
    link_to_user.short_description = _('User')


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReaction, CommentReactionAdmin)
