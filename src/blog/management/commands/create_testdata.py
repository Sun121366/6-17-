from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from blog.models import Article, Category, SideBar, Tag


# [TWL/唐文龙] 首页演示内容集中在这里，方便统一修改并保持重复执行后的数据一致。
ARTICLE_SEEDS = [
    {
        "title": "Django 项目结构与 MTV 架构",
        "summary": "DjangoBlog 按账号、博客、评论、OAuth 和服务器管理等应用拆分功能，请求会依次经过 URL、View、Model 和 Template。",
        "points": ["URL 路由负责匹配路径", "View 处理业务逻辑", "Model 提供数据访问", "Template 完成页面渲染"],
        "tags": ["Django", "MTV", "模板渲染"],
        "views": 180,
    },
    {
        "title": "BlogUser 自定义用户模型",
        "summary": "项目使用自定义 BlogUser 扩展 Django 默认用户，统一关联文章、评论和第三方登录信息。",
        "points": ["继承 AbstractUser", "增加昵称和来源字段", "通过 AUTH_USER_MODEL 生效"],
        "tags": ["用户模型", "Django", "ORM"],
        "views": 165,
    },
    {
        "title": "Article、Category、Tag 数据模型关系",
        "summary": "文章、分类和标签共同组成博客的核心数据模型，分别表达内容主体、目录层级和内容主题。",
        "points": ["Article 与 Category 是多对一", "Article 与 Tag 是多对多", "Category 通过自关联形成树形结构"],
        "tags": ["文章管理", "数据库设计", "ORM"],
        "views": 150,
    },
    {
        "title": "MySQL 数据库配置",
        "summary": "项目默认使用 MySQL，并通过环境变量读取数据库名、账号、密码和连接地址。",
        "points": ["字符集使用 utf8mb4", "开发时连接 127.0.0.1", "部署时通过环境变量覆盖连接信息"],
        "tags": ["MySQL", "数据库设计", "部署"],
        "views": 135,
    },
    {
        "title": "Django ORM 外键与多对多",
        "summary": "Django ORM 将 Python 模型关系映射到数据库表、外键字段和中间关系表。",
        "points": ["ForeignKey 表示一对多", "ManyToManyField 生成中间表", "on_delete 控制级联行为"],
        "tags": ["ORM", "数据库设计", "Django"],
        "views": 122,
    },
    {
        "title": "热门文章统计",
        "summary": "侧边栏热门文章按浏览量倒序查询，用于帮助读者快速定位项目中访问量较高的内容。",
        "points": ["过滤已发布文章", "按 views 倒序排列", "限制侧边栏展示数量"],
        "tags": ["热门文章", "文章管理", "ORM"],
        "views": 110,
    },
    {
        "title": "标签云展示",
        "summary": "标签云统计每个标签关联的文章数量，并根据数量调整显示大小，形成直观的主题入口。",
        "points": ["按文章数排序", "计算标签展示权重", "在模板中渲染标签链接"],
        "tags": ["标签云", "模板渲染", "前端交互"],
        "views": 98,
    },
    {
        "title": "分类树与子类目导航",
        "summary": "分类模型通过 parent_category 自关联形成父子关系，导航栏据此展示可展开的子类目。",
        "points": ["父分类作为一级入口", "子分类显示文章数量", "点击后进入分类归档页"],
        "tags": ["子类目", "Django", "模板渲染"],
        "views": 86,
    },
    {
        "title": "文章列表与分页",
        "summary": "首页和归档页复用文章列表逻辑，通过分页避免一次加载过多内容。",
        "points": ["ArticleListView 组织列表数据", "模板复用文章卡片", "分页组件生成上一页和下一页链接"],
        "tags": ["文章管理", "模板渲染", "Django"],
        "views": 75,
    },
    {
        "title": "评论与回复",
        "summary": "评论模型记录评论用户、所属文章和父评论，从而支持顶层评论与嵌套回复。",
        "points": ["author 指向评论用户", "article 指向所属文章", "parent_comment 表达回复关系"],
        "tags": ["评论系统", "ORM", "数据库设计"],
        "views": 66,
    },
    {
        "title": "Emoji 评论反应",
        "summary": "评论反应记录用户对某条评论的 Emoji 类型，并通过唯一约束避免重复反应。",
        "points": ["记录评论和用户", "保存反应类型", "unique_together 保证数据唯一"],
        "tags": ["评论系统", "前端交互", "数据库设计"],
        "views": 58,
    },
    {
        "title": "OAuth 第三方登录",
        "summary": "OAuthUser 保存第三方平台身份，OAuthConfig 保存平台客户端配置，两者共同支持第三方登录。",
        "points": ["第三方账号可绑定站内用户", "平台配置集中管理", "登录流程与本地账号解耦"],
        "tags": ["OAuth", "用户模型", "Django"],
        "views": 51,
    },
    {
        "title": "友情链接与公告",
        "summary": "侧边栏支持友情链接和自定义公告内容，方便扩展课程项目的外部资源与说明信息。",
        "points": ["Links 控制链接排序和展示位置", "SideBar 保存自定义内容", "模板按顺序渲染侧边内容"],
        "tags": ["后台管理", "模板渲染", "Django"],
        "views": 44,
    },
    {
        "title": "BlogSettings 全局配置",
        "summary": "BlogSettings 统一保存站点名称、SEO、主题颜色、备案信息和页眉页脚等全局配置。",
        "points": ["站点信息集中维护", "clean 方法限制单例配置", "前台模板读取统一配置"],
        "tags": ["后台管理", "SEO", "模板渲染"],
        "views": 38,
    },
    {
        "title": "Admin 后台管理",
        "summary": "Django Admin 提供用户、文章、分类、标签、评论和站点配置的后台管理入口。",
        "points": ["后台模型注册", "支持列表筛选和搜索", "统一管理业务数据"],
        "tags": ["后台管理", "Django", "用户模型"],
        "views": 33,
    },
    {
        "title": "搜索功能",
        "summary": "项目通过 Haystack 接入 Whoosh 或 Elasticsearch，为文章标题和正文提供搜索入口。",
        "points": ["索引模型字段", "搜索视图处理查询参数", "搜索结果复用了文章展示组件"],
        "tags": ["搜索", "测试", "Django"],
        "views": 28,
    },
    {
        "title": "SEO 元数据优化",
        "summary": "文章详情、分类页和标签页会生成标题、描述与关键词，便于搜索引擎理解页面内容。",
        "points": ["从正文提取描述", "从标签生成关键词", "通过模板输出 meta 信息"],
        "tags": ["SEO", "模板渲染", "前端交互"],
        "views": 24,
    },
    {
        "title": "Vite 前端构建",
        "summary": "前端使用 Vite 管理 Tailwind CSS、Alpine.js 和 HTMX 等资源，并与 Django 模板协作。",
        "points": ["开发模式连接 Vite 服务", "生产模式输出压缩资源", "模板通过自定义标签加载资源"],
        "tags": ["前端交互", "部署", "Django"],
        "views": 20,
    },
    {
        "title": "部署与运行验证",
        "summary": "部署时需要配置数据库、静态资源、缓存和运行环境，并通过健康检查接口确认服务状态。",
        "points": ["配置 MySQL 连接", "收集静态资源", "访问 health 接口检查服务"],
        "tags": ["部署", "测试", "MySQL"],
        "views": 17,
    },
]

ARTICLE_TAGS = {tag for seed in ARTICLE_SEEDS for tag in seed["tags"]}


def _get_or_rename_category(new_name, old_names, parent=None):
    """优先复用旧分类对象，避免改名时破坏已有文章关系。"""
    category = Category.objects.filter(name=new_name).first()
    if category:
        if category.parent_category_id != getattr(parent, "id", None):
            category.parent_category = parent
            category.save(update_fields=["parent_category"])
        return category

    for old_name in old_names:
        category = Category.objects.filter(name=old_name).first()
        if category:
            category.name = new_name
            category.parent_category = parent
            category.save(update_fields=["name", "parent_category"])
            return category

    return Category.objects.create(name=new_name, parent_category=parent)


class Command(BaseCommand):
    help = "Create or refresh the homepage demo articles"

    @transaction.atomic
    def handle(self, *args, **options):
        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(
            email="test@test.com",
            username="测试用户",
            defaults={"password": make_password("test!q@w#eTYU")},
        )
        user.set_password("test!q@w#eTYU")
        user.save(update_fields=["password"])

        # [TWL/唐文龙] 保留旧分类对象并改名，已有文章外键不需要重新绑定。
        parent = _get_or_rename_category(
            "项目开发", ["总类", "我是父类目", "父类目"], parent=None)
        category = _get_or_rename_category(
            "Django 博客", ["子类目"], parent=parent)

        # [TWL/唐文龙] 用项目相关说明替换侧边栏示例卡片，保留原有展示位置。
        sidebar_items = [
            (
                "DjangoBlog 项目说明",
                "本项目基于 DjangoBlog 开源项目进行课程实践，重点展示文章、分类、标签、评论与后台管理功能。",
            ),
            (
                "Django 官方文档",
                "[查看 Django 官方文档](https://docs.djangoproject.com/zh-hans/5.2/)",
            ),
        ]
        for sequence, (name, content) in enumerate(sidebar_items, start=1):
            SideBar.objects.update_or_create(
                sequence=sequence,
                defaults={"name": name, "content": content, "is_enable": True},
            )

        for index, seed in enumerate(ARTICLE_SEEDS, start=1):
            article = (
                Article.objects.filter(title=seed["title"]).first()
                or Article.objects.filter(title=f"nice title {index}").first()
                or Article(title=seed["title"])
            )
            article.title = seed["title"]
            article.body = f'{seed["summary"]}\n\n实现要点：{"；".join(seed["points"])}。'
            article.category = category
            article.author = user
            article.status = "p"
            article.type = "a"
            article.views = seed["views"]
            article.save()

            tags = [
                Tag.objects.get_or_create(name=name)[0]
                for name in seed["tags"]
            ]
            article.tags.set(tags)

        # [TWL/唐文龙] 清理旧演示标签，只删除已经没有任何文章引用的数据。
        legacy_tags = Tag.objects.filter(Q(name="标签") | Q(name__regex=r"^标签\d+$"))
        for tag in legacy_tags:
            if tag.name not in ARTICLE_TAGS and not tag.article_set.exists():
                tag.delete()

        from djangoblog.utils import cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS("created or refreshed test datas"))
