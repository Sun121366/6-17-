# szj: ===== comments 应用 · 路由配置（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 本模块把评论相关的两个视图挂到 URL 上，统一由 djangoblog/urls.py 以根路径包含：
# szj:   POST /article/<article_id>/postcomment —— 提交评论 / 回复
# szj:   GET|POST /comment/<comment_id>/react    —— 查询或切换 Emoji 反应
# szj: 路由名（name）供模板与测试通过 reverse('comments:xxx') 反向解析，避免硬编码 URL。
"""评论应用路由配置。"""

from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    # szj: 提交评论/回复：路径与视图方法名保持一致，便于理解与排查。
    path(
        'article/<int:article_id>/postcomment',
        views.CommentPostView.as_view(),
        name='postcomment'),
    # szj: Emoji 反应：GET 查询统计，POST 切换点赞状态，同一个 URL 两种语义。
    path(
        'comment/<int:comment_id>/react',
        views.CommentReactionView.as_view(),
        name='comment_react'),
]
