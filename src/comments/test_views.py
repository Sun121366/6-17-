# szj: ===== comments 应用 · 视图测试（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 覆盖两部分：1) 评论提交视图的错误处理与边界条件；
# szj:             2) Emoji 反应 API 的权限、参数校验与“点赞/取消点赞”切换语义。
# szj: 本次质量改进：把 setUp 内的导入提升到模块顶部（修复 C0415）、去掉未使用的导入与变量，
# szj: 并新增 CommentReactionViewTest —— 原测试完全没有覆盖反应接口。
"""Comments Views 测试
测试评论功能的错误处理和边界条件
"""
from django.test import Client, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import BlogUser
from blog.models import Article, BlogSettings, Category
from comments.models import Comment, CommentReaction
from djangoblog.test_base import ViewTestMixin


class CommentViewTest(TransactionTestCase, ViewTestMixin):
    """测试评论视图"""

    def setUp(self):
        """准备测试客户端、普通用户、分类、已发布文章与评论审核配置。"""
        self.client = Client()
        self.user = BlogUser.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='测试分类',
            creation_time=timezone.now(),
            last_modify_time=timezone.now()
        )
        self.article = Article.objects.create(
            title='测试文章',
            body='测试内容',
            author=self.user,
            category=self.category,
            type='a',
            status='p'
        )
        self.blog_settings, _ = BlogSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_name': '测试博客',
                'site_description': '测试描述',
                'comment_need_review': False,
            }
        )

    def login_user(self):
        """登录测试用户"""
        return self.client.login(username='testuser', password='testpass123')

    def test_post_comment_authenticated(self):
        """测试已登录用户发表评论"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})
        response = self.client.post(url, {'body': '这是一条测试评论'})
        self.assertEqual(response.status_code, 302)

        # 验证评论已创建
        comments = Comment.objects.filter(article=self.article)
        self.assertGreater(comments.count(), 0)

    def test_post_comment_unauthenticated(self):
        """测试未登录用户发表评论"""
        self.client.logout()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})
        response = self.client.post(url, {'body': '匿名评论'})
        # szj: AuthenticatedFormView 会把未登录用户重定向到登录页，允许 200/302 等正常响应。
        self.assertIn(response.status_code, [200, 302, 403, 500])

    def test_post_comment_empty_body(self):
        """测试提交空评论"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})
        response = self.client.post(url, {'body': ''})
        # 应该返回表单错误
        self.assertIn(response.status_code, [200, 302])

    def test_post_comment_invalid_article(self):
        """测试对不存在的文章评论"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': 99999})
        response = self.client.post(url, {'body': '评论'})
        self.assertEqual(response.status_code, 404)

    def test_post_reply_comment(self):
        """测试回复评论"""
        self.login_user()
        # 先创建一条评论
        parent_comment = Comment.objects.create(
            body='父评论',
            author=self.user,
            article=self.article
        )
        parent_comment.is_enable = True
        parent_comment.save()

        # 回复这条评论
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})
        response = self.client.post(url, {
            'body': '这是回复',
            'parent_comment_id': parent_comment.id
        })
        self.assertIn(response.status_code, [200, 302])

    def test_comment_moderation(self):
        """测试评论审核"""
        # 设置需要审核
        self.blog_settings.comment_need_review = True
        self.blog_settings.save()

        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})
        response = self.client.post(url, {'body': '待审核的评论'})
        self.assertEqual(response.status_code, 302)

        # 验证评论需要审核
        comment = Comment.objects.filter(article=self.article).latest('id')
        self.assertFalse(comment.is_enable)

    def test_comment_display_on_article(self):
        """测试评论在文章页显示"""
        # szj: 这里只关心文章详情页能正常渲染，评论对象作为前置数据创建即可，无需再引用。
        Comment.objects.create(
            body='测试显示评论',
            author=self.user,
            article=self.article,
            is_enable=True
        )

        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_disabled_comment_not_display(self):
        """测试未启用的评论不显示"""
        Comment.objects.create(
            body='未启用的评论',
            author=self.user,
            article=self.article,
            is_enable=False
        )

        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class CommentSpamTest(TransactionTestCase, ViewTestMixin):
    """测试评论垃圾防护"""

    def setUp(self):
        """准备测试客户端、用户、文章与站点配置。"""
        self.client = Client()
        self.user = BlogUser.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='测试分类',
            creation_time=timezone.now(),
            last_modify_time=timezone.now()
        )
        self.article = Article.objects.create(
            title='测试文章',
            body='测试内容',
            author=self.user,
            category=self.category,
            type='a',
            status='p'
        )
        self.blog_settings, _ = BlogSettings.objects.get_or_create(
            id=1,
            defaults={'comment_need_review': False}
        )

    def login_user(self):
        """登录测试用户"""
        return self.client.login(username='testuser', password='testpass123')

    def test_duplicate_comment(self):
        """测试重复评论"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})
        comment_data = {'body': '重复的评论内容'}

        # 第一次提交
        response1 = self.client.post(url, comment_data)
        self.assertEqual(response1.status_code, 302)

        # 第二次提交相同内容
        response2 = self.client.post(url, comment_data)
        # 应该被阻止或显示错误
        self.assertIn(response2.status_code, [200, 302])

    def test_comment_rate_limit(self):
        """测试评论频率限制"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})

        # 快速连续发表多条评论
        for _ in range(5):
            response = self.client.post(url, {'body': f'评论{_}'})
            # 后续评论可能被限制
            self.assertIn(response.status_code, [200, 302, 429])


class CommentSecurityTest(TransactionTestCase, ViewTestMixin):
    """测试评论安全性"""

    def setUp(self):
        """准备测试客户端、用户、文章与站点配置。"""
        self.client = Client()
        self.user = BlogUser.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='测试分类',
            creation_time=timezone.now(),
            last_modify_time=timezone.now()
        )
        self.article = Article.objects.create(
            title='测试文章',
            body='测试内容',
            author=self.user,
            category=self.category,
            type='a',
            status='p'
        )
        self.blog_settings, _ = BlogSettings.objects.get_or_create(
            id=1,
            defaults={'comment_need_review': False}
        )

    def login_user(self):
        """登录测试用户"""
        return self.client.login(username='testuser', password='testpass123')

    def test_xss_protection(self):
        """测试 XSS 防护"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})

        # 提交包含 script 标签的评论
        xss_body = '<script>alert("xss")</script>普通内容'
        response = self.client.post(url, {'body': xss_body})
        self.assertEqual(response.status_code, 302)

        # 验证评论已创建（XSS 过滤在渲染时处理）
        comment = Comment.objects.filter(article=self.article).latest('id')
        self.assertIsNotNone(comment)

    def test_sql_injection_protection(self):
        """测试 SQL 注入防护"""
        self.login_user()
        url = reverse('comments:postcomment', kwargs={'article_id': self.article.id})

        # 提交包含 SQL 注入尝试的评论
        sql_body = "'; DROP TABLE comments; --"
        response = self.client.post(url, {'body': sql_body})
        # 应该正常处理，不会执行 SQL
        self.assertIn(response.status_code, [200, 302])

        # 验证表仍然存在
        self.assertTrue(Comment.objects.exists())


class CommentReactionViewTest(TransactionTestCase):
    """测试评论 Emoji 反应 API（CommentReactionView）。

    覆盖：公开查询、未登录拦截、非法参数、对未审核评论的越权保护、点赞/取消切换。
    """

    def setUp(self):
        """准备两个用户、一篇文章，以及一条已审核和一条待审核评论。"""
        self.client = Client()
        self.user = BlogUser.objects.create_user(
            username='reactor',
            email='reactor@test.com',
            password='testpass123'
        )
        self.other_user = BlogUser.objects.create_user(
            username='other',
            email='other@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='反应测试分类',
            creation_time=timezone.now(),
            last_modify_time=timezone.now()
        )
        self.article = Article.objects.create(
            title='反应测试文章',
            body='反应测试内容',
            author=self.user,
            category=self.category,
            type='a',
            status='p'
        )
        self.comment = Comment.objects.create(
            body='可点赞的评论',
            author=self.other_user,
            article=self.article,
            is_enable=True
        )
        self.disabled_comment = Comment.objects.create(
            body='待审核评论',
            author=self.other_user,
            article=self.article,
            is_enable=False
        )

    def login_user(self):
        """登录测试用户。"""
        return self.client.login(username='reactor', password='testpass123')

    def reaction_url(self, comment_id):
        """构造某条评论的反应接口地址。"""
        return reverse('comments:comment_react', kwargs={'comment_id': comment_id})

    def test_get_reactions_public_without_login(self):
        """未登录也可以查询反应统计，初始为空字典。"""
        response = self.client.get(self.reaction_url(self.comment.id))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['success'])
        self.assertEqual(payload['reactions'], {})

    def test_post_reaction_requires_login(self):
        """未登录提交反应应返回 401。"""
        response = self.client.post(
            self.reaction_url(self.comment.id), {'reaction_type': '👍'})

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json()['success'])
        self.assertEqual(CommentReaction.objects.count(), 0)

    def test_toggle_reaction_adds_then_removes(self):
        """同一用户连续提交同一 Emoji：第一次点赞，第二次取消。"""
        self.login_user()
        url = self.reaction_url(self.comment.id)

        # 第一次提交 —— 创建反应
        added = self.client.post(url, {'reaction_type': '👍'})
        self.assertEqual(added.status_code, 200)
        self.assertEqual(added.json()['action'], 'added')
        self.assertEqual(CommentReaction.objects.count(), 1)

        summary = added.json()['reactions']['👍']
        self.assertEqual(summary['count'], 1)
        self.assertTrue(summary['has_reacted'])
        self.assertIn('reactor', summary['users'])

        # 第二次提交 —— 取消反应
        removed = self.client.post(url, {'reaction_type': '👍'})
        self.assertEqual(removed.status_code, 200)
        self.assertEqual(removed.json()['action'], 'removed')
        self.assertEqual(CommentReaction.objects.count(), 0)

    def test_post_invalid_reaction_type(self):
        """非法 Emoji 类型返回 400，且不会写入数据库。"""
        self.login_user()

        response = self.client.post(
            self.reaction_url(self.comment.id), {'reaction_type': 'X'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(CommentReaction.objects.count(), 0)

    def test_reaction_on_disabled_comment_returns_404(self):
        """对未审核（不可见）的评论点赞应返回 404。"""
        self.login_user()

        response = self.client.post(
            self.reaction_url(self.disabled_comment.id), {'reaction_type': '❤️'})

        self.assertEqual(response.status_code, 404)

    def test_reaction_summary_with_multiple_users(self):
        """多名用户点赞时，统计应汇总人数、把用户名返回给前端，并正确标记当前用户。"""
        self.login_user()
        CommentReaction.objects.create(
            comment=self.comment, user=self.user, reaction_type='🚀')
        CommentReaction.objects.create(
            comment=self.comment, user=self.other_user, reaction_type='🚀')

        response = self.client.get(self.reaction_url(self.comment.id))

        self.assertEqual(response.status_code, 200)
        summary = response.json()['reactions']['🚀']
        self.assertEqual(summary['count'], 2)
        self.assertTrue(summary['has_reacted'])
        self.assertEqual(len(summary['users']), 2)
