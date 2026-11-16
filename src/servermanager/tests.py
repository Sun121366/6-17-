"""servermanager 应用测试。

cgw: 第9-10周补充。原有用例只覆盖微信机器人流程，且 ``test_chat_gpt`` 只断言
返回值非 None，接口失败后返回的"服务器出错了"同样满足断言，缺陷因而长期未
被发现。本次为命令执行、大模型调用与运维助手页面补齐可区分成功与失败的用例。
"""

import os
import subprocess
from unittest import mock

from django.test import TestCase
from werobot.messages.messages import TextMessage

from accounts.models import BlogUser
from blog.models import Category, Article
from djangoblog.test_base import BaseTestCase
from servermanager.api.commonapi import ChatGPT, CommandHandler
from servermanager.models import commands
from .robot import MessageHandler
from .robot import search, category, recents

# cgw: 被测模块中 subprocess 的补丁目标，集中定义避免测试里写死字符串
SUBPROCESS_RUN = 'servermanager.api.commonapi.subprocess.run'


class ChatGPTTest(TestCase):
    """大模型问答封装的用例。"""

    @staticmethod
    def _client_returning(content):
        """构造一个返回固定回答的假客户端。"""
        fake = mock.Mock()
        fake.chat.completions.create.return_value = mock.Mock(
            choices=[mock.Mock(message=mock.Mock(content=content))]
        )
        return fake

    def test_missing_api_key_returns_hint(self):
        """未配置密钥时应如实提示，而不是返回失败文案。"""
        with mock.patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            bot = ChatGPT()
            self.assertFalse(bot.is_configured())
            self.assertIn('OPENAI_API_KEY', bot.ask('你好'))

    def test_config_read_from_environment(self):
        """密钥、接口地址、模型名均可由环境变量覆盖。"""
        with mock.patch.dict(os.environ, {
            'OPENAI_API_KEY': 'env-key',
            'OPENAI_BASE_URL': 'https://example.com/v1',
            'OPENAI_MODEL': 'qwen-plus',
        }):
            bot = ChatGPT()
            self.assertTrue(bot.is_configured())
            self.assertEqual(bot.api_key, 'env-key')
            self.assertEqual(bot.base_url, 'https://example.com/v1')
            self.assertEqual(bot.model, 'qwen-plus')

    def test_empty_prompt(self):
        """空问题直接拒绝，不发起请求。"""
        self.assertEqual(ChatGPT(api_key='k').ask('   '), '问题内容为空，请重新输入')

    def test_ask_success(self):
        """正常返回时去掉首尾空白后原文给出。"""
        bot = ChatGPT(api_key='k')
        bot._client = self._client_returning(' 这是回答 ')
        self.assertEqual(bot.ask('问题'), '这是回答')

    def test_ask_api_error(self):
        """接口异常时返回可读提示，且与成功结果可区分。"""
        bot = ChatGPT(api_key='k')
        fake = mock.Mock()
        fake.chat.completions.create.side_effect = Exception('boom')
        bot._client = fake
        self.assertEqual(bot.ask('问题'), 'AI 服务暂时不可达，请稍后重试')

    def test_ask_empty_choices(self):
        """响应缺少 choices 时不抛异常。"""
        bot = ChatGPT(api_key='k')
        fake = mock.Mock()
        fake.chat.completions.create.return_value = mock.Mock(choices=[])
        bot._client = fake
        self.assertEqual(bot.ask('问题'), 'AI 未返回有效回答')

    def test_ask_empty_content(self):
        """响应正文为空时不抛异常。"""
        bot = ChatGPT(api_key='k')
        bot._client = self._client_returning('')
        self.assertEqual(bot.ask('问题'), 'AI 未返回有效回答')

    def test_class_level_chat(self):
        """类级入口沿用环境变量配置，未配置时给出提示。"""
        with mock.patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            self.assertIn('OPENAI_API_KEY', ChatGPT.chat('你好'))


class CommandHandlerTest(TestCase):
    """运维命令查询与执行的用例。"""

    def test_lazy_command_loading(self):
        """构造时不查询命令表，避免导入期访问数据库。"""
        self.assertIsNone(CommandHandler()._commands)

    def test_run_matches_title_case_insensitively(self):
        """按标题查找命令时忽略大小写。"""
        commands.objects.create(title='LIST', command='echo toc-run', describe='列出')
        self.assertEqual(CommandHandler().run('list'), 'toc-run')

    def test_run_unknown_title(self):
        """标题不存在时给出帮助提示。"""
        self.assertIn('未找到相关命令', CommandHandler().run('not-exist'))

    def test_refresh_reloads_commands(self):
        """refresh 后能读到新增命令。"""
        handler = CommandHandler()
        self.assertEqual(len(handler.commands), 0)
        commands.objects.create(title='NEW', command='echo 1', describe='新增')
        self.assertEqual(len(handler.refresh()), 1)

    def test_whitelist_rejects_unknown_command(self):
        """不在白名单的命令被拒绝。"""
        result = CommandHandler(whitelist=('echo',)).execute('rm -rf /tmp/anything')
        self.assertIn('不在允许列表', result)

    def test_whitelist_allows_echo(self):
        """白名单内的命令正常执行并返回输出。"""
        result = CommandHandler(whitelist=('echo',)).execute('echo toc-echo')
        self.assertEqual(result, 'toc-echo')

    def test_empty_command(self):
        """空白命令直接拒绝。"""
        self.assertIn('命令为空', CommandHandler().execute('   '))

    def test_malformed_command(self):
        """引号不闭合导致无法拆分时按非法命令处理。"""
        self.assertIn('命令为空', CommandHandler().execute('echo "unclosed'))

    def test_timeout(self):
        """执行超时时返回明确提示。"""
        with mock.patch(SUBPROCESS_RUN, side_effect=subprocess.TimeoutExpired('echo', 1)):
            result = CommandHandler(whitelist=('echo',), timeout=1).execute('echo x')
        self.assertIn('超时', result)

    def test_command_not_found(self):
        """命令不存在时提示命令缺失。"""
        with mock.patch(SUBPROCESS_RUN, side_effect=FileNotFoundError()):
            result = CommandHandler(whitelist=('echo',)).execute('echo x')
        self.assertIn('命令不存在', result)

    def test_permission_error(self):
        """无执行权限时提示权限不足。"""
        with mock.patch(SUBPROCESS_RUN, side_effect=PermissionError()):
            result = CommandHandler(whitelist=('echo',)).execute('echo x')
        self.assertIn('没有权限', result)

    def test_output_truncated(self):
        """超长输出被截断并标注。"""
        completed = mock.Mock(stdout='x' * 9000, stderr='')
        with mock.patch(SUBPROCESS_RUN, return_value=completed):
            result = CommandHandler(whitelist=('echo',)).execute('echo x')
        self.assertIn('输出已截断', result)

    def test_no_output(self):
        """无输出时给出说明而不是空串。"""
        completed = mock.Mock(stdout='', stderr='')
        with mock.patch(SUBPROCESS_RUN, return_value=completed):
            result = CommandHandler(whitelist=('echo',)).execute('echo x')
        self.assertEqual(result, '命令已执行，无输出')

    def test_stderr_merged(self):
        """标准错误与标准输出一起返回。"""
        completed = mock.Mock(stdout='out', stderr='err')
        with mock.patch(SUBPROCESS_RUN, return_value=completed):
            result = CommandHandler(whitelist=('echo',)).execute('echo x')
        self.assertIn('out', result)
        self.assertIn('err', result)

    def test_get_help_contains_description(self):
        """帮助信息包含命令标题与描述。"""
        commands.objects.create(title='AAA', command='echo 1', describe='说明A')
        self.assertIn('AAA:说明A', CommandHandler().get_help())


class ConsoleViewTest(BaseTestCase):
    """运维助手页面用例。"""

    URL = '/servermanager/console/'

    def setUp(self):
        super().setUp()
        commands.objects.create(
            title='DEMO',
            command='echo toc-demo-output',
            describe='示例命令',
        )

    def test_anonymous_redirected_to_login(self):
        """未登录访问跳转登录页。"""
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_non_staff_forbidden(self):
        """普通用户无权限访问。"""
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.URL).status_code, 403)

    def test_staff_can_open_page(self):
        """管理员可打开页面并看到已登记命令。"""
        self.client.force_login(self.admin_user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '运维助手')
        self.assertContains(response, 'DEMO')

    def test_post_registered_command(self):
        """选择已登记命令后返回执行结果。"""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.URL, {'action': 'registered', 'title': 'DEMO'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'toc-demo-output')

    def test_post_registered_without_selection(self):
        """未选择命令时给出提示而不是执行。"""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.URL, {'action': 'registered', 'title': ''})
        self.assertContains(response, '请选择一条已登记的命令')

    def test_post_free_command_allowed(self):
        """白名单内的命令可以执行。"""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.URL, {'action': 'free', 'command': 'echo toc-free'})
        self.assertContains(response, 'toc-free')

    def test_post_free_command_denied(self):
        """白名单外的命令被拒绝。"""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.URL, {'action': 'free', 'command': 'rm -rf /tmp/anything'})
        self.assertContains(response, '不在允许列表')

    def test_post_chat_without_api_key(self):
        """未配置密钥时页面给出配置提示。"""
        self.client.force_login(self.admin_user)
        with mock.patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            response = self.client.post(self.URL, {'action': 'chat', 'prompt': '你好'})
        self.assertContains(response, 'OPENAI_API_KEY')

    def test_post_chat_blank_prompt(self):
        """空问题不通过表单校验。"""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.URL, {'action': 'chat', 'prompt': ''})
        self.assertContains(response, '不合法')

    def test_post_unknown_action(self):
        """未知动作给出提示。"""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.URL, {'action': 'unknown'})
        self.assertContains(response, '未知的操作类型')


class ServerManagerTest(TestCase):
    """微信机器人既有用例，保持原有覆盖范围。"""

    def setUp(self):
        self.client = self.client_class()

    def test_validate_comment(self):
        user = BlogUser.objects.create_superuser(
            email="liangliangyy1@gmail.com",
            username="liangliangyy1",
            password="liangliangyy1")

        self.client.login(username='liangliangyy1', password='liangliangyy1')

        c = Category()
        c.name = "categoryccc"
        c.save()

        article = Article()
        article.title = "nicetitleccc"
        article.body = "nicecontentccc"
        article.author = user
        article.category = c
        article.type = 'a'
        article.status = 'p'
        article.save()
        s = TextMessage([])
        s.content = "nice"
        rsp = search(s, None)
        rsp = category(None, None)
        self.assertIsNotNone(rsp)
        rsp = recents(None, None)
        self.assertTrue(rsp != '暂时还没有文章')

        cmd = commands()
        cmd.title = "test"
        cmd.command = "ls"
        cmd.describe = "test"
        cmd.save()

        cmdhandler = CommandHandler()
        rsp = cmdhandler.run('test')
        self.assertIsNotNone(rsp)
        s.source = 'u'
        s.content = 'test'
        msghandler = MessageHandler(s, {})

        msghandler.handler()
        s.content = 'y'
        msghandler.handler()
        s.content = 'idcard:12321233'
        msghandler.handler()
        s.content = 'weather:上海'
        msghandler.handler()
        s.content = 'admin'
        msghandler.handler()
        s.content = '123'
        msghandler.handler()

        s.content = 'exit'
        msghandler.handler()
