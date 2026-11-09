# szj: ===== comments 应用 · 应用配置（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: Django 启动时通过 AppConfig 读取应用元信息；这里补充中文 verbose_name，
# szj: 让后台“应用”分组名称直接显示为中文。
"""comments 应用的配置入口。

Django 在 INSTALLED_APPS 中加载 'comments' 时会读取本配置类，
其中 name 必须是应用的 Python 包名，verbose_name 决定后台展示名称。
"""

from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """评论应用配置类：声明应用名称与后台中文显示名。"""

    name = 'comments'
    verbose_name = '评论'
