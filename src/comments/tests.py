# szj: ===== comments 应用 · 集成测试（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 本文件覆盖“提交评论 → 审核 → 展示 → 模板树解析 → 邮件通知”的完整链路。
# szj: 本次质量改进：去掉通配符导入改为显式导入（pylint W0401），
# szj: 把函数内导入提升到模块顶部（C0415），并补齐模块/类/方法 docstring。
"""评论应用集成测试。

覆盖评论提交、审核开关、嵌套回复、评论树模板标签与邮件通知工具，
使用 TransactionTestCase 保证每条用例结束后数据库回到干净状态。
"""

from django.test import Client, RequestFactory, TransactionTestCase
from django.urls import reverse

from accounts.models import BlogUser
from blog.models import Article, BlogSettings, Category
from comments.models import Comment
from comments.templatetags.comments_tags import parse_commenttree, show_comment_item
from comments.utils import send_comment_email
from djangoblog.utils import get_max_articleid_commentid


# Create your tests here.

class CommentsTest(TransactionTestCase):
    """评论主流程集成测试。"""

    def setUp(self):
        """准备测试客户端、请求工厂、站点审核配置与超级用户。"""
        self.client = Client()
        self.factory = RequestFactory()
        value = BlogSettings()
        value.comment_need_review = True
        value.save()

        self.user = BlogUser.objects.create_superuser(
            email="liangliangyy1@gmail.com",
            username="liangliangyy1",
            password="liangliangyy1")

    def update_article_comment_status(self, article):
        """把某篇文章下的所有评论批量置为“已通过审核”，模拟管理员审核通过。"""
        comments = article.comment_set.all()
        for comment in comments:
            comment.is_enable = True
            comment.save()

    def test_validate_comment(self):
        """验证评论从提交到展示的完整流程（含审核与嵌套回复）。"""
        self.client.login(username='liangliangyy1', password='liangliangyy1')

        category = Category()
        category.name = "categoryccc"
        category.save()

        article = Article()
        article.title = "nicetitleccc"
        article.body = "nicecontentccc"
        article.author = self.user
        article.category = category
        article.type = 'a'
        article.status = 'p'
        article.save()

        comment_url = reverse(
            'comments:postcomment', kwargs={
                'article_id': article.id})

        response = self.client.post(comment_url,
                                    {
                                        'body': '123ffffffffff'
                                    })

        self.assertEqual(response.status_code, 302)

        # szj: 站点开启了“评论需要审核”，因此刚提交的评论不应出现在前台列表中。
        article = Article.objects.get(pk=article.pk)
        self.assertEqual(len(article.comment_list()), 0)
        self.update_article_comment_status(article)

        self.assertEqual(len(article.comment_list()), 1)

        response = self.client.post(comment_url,
                                    {
                                        'body': '123ffffffffff',
                                    })

        self.assertEqual(response.status_code, 302)

        article = Article.objects.get(pk=article.pk)
        self.update_article_comment_status(article)
        self.assertEqual(len(article.comment_list()), 2)
        parent_comment_id = article.comment_list()[0].id

        # szj: 提交一条带 Markdown 语法的回复，验证 markdown 内容可正常入库。
        response = self.client.post(comment_url,
                                    {
                                        'body': '''
                                        # Title1

        ```python
        import os
        ```

        [url](https://www.lylinux.net/)

        [ddd](http://www.baidu.com)


        ''',
                                        'parent_comment_id': parent_comment_id
                                    })

        self.assertEqual(response.status_code, 302)
        self.update_article_comment_status(article)
        article = Article.objects.get(pk=article.pk)
        self.assertEqual(len(article.comment_list()), 3)
        comment = Comment.objects.get(id=parent_comment_id)
        # szj: 模板标签 parse_commenttree 应能解析出父评论下的 1 条子评论。
        tree = parse_commenttree(article.comment_list(), comment)
        self.assertEqual(len(tree), 1)
        # szj: inclusion tag 返回渲染上下文，depth 由 ischild 决定。
        data = show_comment_item(comment, True)
        self.assertIsNotNone(data)
        s = get_max_articleid_commentid()
        self.assertIsNotNone(s)

        send_comment_email(comment)
