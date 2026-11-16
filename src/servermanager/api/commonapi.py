"""服务器管理相关的外部接口封装。

本模块集中两个能力：运维命令的查询与执行、大模型问答调用。两者都要求
显式配置后才可用，未配置时返回明确提示，不再静默降级。

cgw: 本次维护重写了命令执行与模型调用的实现，模型接口由 openai 0.x
语法迁移到 1.x/2.x 客户端，并补充了白名单校验与超时控制。
"""

import logging
import os
import shlex
import subprocess

from django.conf import settings

from servermanager.models import commands

logger = logging.getLogger(__name__)

# cgw: 命令执行与大模型请求的默认超时（秒），可在 settings 中覆盖
DEFAULT_TIMEOUT = 15
# cgw: 单次命令输出保留的最大字符数，避免超长输出占满内存与页面
MAX_OUTPUT_LENGTH = 8000
# cgw: 未显式配置白名单时仅允许这些只读命令
DEFAULT_COMMAND_WHITELIST = (
    'ls', 'pwd', 'whoami', 'df', 'du', 'uptime', 'date',
    'echo', 'cat', 'head', 'tail', 'wc', 'uname',
)


class ChatGPT:
    """大模型问答接口。

    兼容任何提供 OpenAI 协议的服务端点：密钥、地址与模型名分别取自
    ``OPENAI_API_KEY``、``OPENAI_BASE_URL``、``OPENAI_MODEL`` 三个环境
    变量，因此官方接口与中转接口都可以直接使用。

    cgw: 原实现使用 ``openai.ChatCompletion`` 顶层接口，该接口在 openai
    1.x 起已被移除，调用必然抛出 AttributeError 并统一返回"服务器出错了"。
    """

    DEFAULT_MODEL = 'gpt-3.5-turbo'

    def __init__(self, api_key=None, base_url=None, model=None, timeout=None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.base_url = base_url or os.environ.get('OPENAI_BASE_URL')
        self.model = model or os.environ.get('OPENAI_MODEL') or self.DEFAULT_MODEL
        self.timeout = timeout or getattr(settings, 'CHATGPT_TIMEOUT', DEFAULT_TIMEOUT)
        self._client = None

    @property
    def client(self):
        """惰性构造客户端。

        只有在真正发起请求时才创建连接，避免模块导入期就校验密钥，
        从而不阻断未配置大模型功能的部署方式。

        :raises RuntimeError: 未配置 ``OPENAI_API_KEY`` 时抛出
        """
        if not self.api_key:
            raise RuntimeError('未配置 OPENAI_API_KEY，AI 问答功能不可用')
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url or None,
                timeout=self.timeout,
            )
        return self._client

    def is_configured(self):
        """是否已具备调用条件，供页面区分"未配置"与"调用失败"。"""
        return bool(self.api_key)

    def ask(self, prompt):
        """向模型提问并返回纯文本回答。

        :param prompt: 用户问题
        :return: 模型回答；任何失败都返回可直接展示的中文提示
        """
        if not isinstance(prompt, str) or not prompt.strip():
            return '问题内容为空，请重新输入'
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                timeout=self.timeout,
            )
        except RuntimeError as exc:
            # cgw: 未配置密钥属于部署问题，记录 warning 并如实告知使用者
            logger.warning('大模型接口未配置：%s', exc)
            return str(exc)
        except Exception as exc:
            logger.error('大模型接口调用失败：%s', exc)
            return 'AI 服务暂时不可达，请稍后重试'
        return self._extract_content(response)

    @staticmethod
    def _extract_content(response):
        """从响应体中取出回答文本，兼容缺失字段的异常返回。"""
        choices = getattr(response, 'choices', None) or []
        if not choices:
            logger.warning('大模型返回结果中不含 choices')
            return 'AI 未返回有效回答'
        message = getattr(choices[0], 'message', None)
        content = getattr(message, 'content', None)
        if not content:
            logger.warning('大模型返回结果中不含正文')
            return 'AI 未返回有效回答'
        return content.strip()

    @classmethod
    def chat(cls, prompt):
        """类级快捷入口，使用环境变量中的默认配置。"""
        return cls().ask(prompt)


class CommandHandler:
    """运维命令的查询与执行。

    命令定义存放在 ``commands`` 表中，执行前必须先通过白名单校验，
    不允许把数据库中的命令串直接交给 shell。

    cgw: 原实现用 ``os.popen`` 执行命令串且无任何校验，命令表被篡改即可
    获得任意命令执行能力；同时实例在模块导入期就会查询数据库。
    """

    def __init__(self, whitelist=None, timeout=None):
        self.whitelist = tuple(
            whitelist or getattr(settings, 'COMMAND_WHITELIST', DEFAULT_COMMAND_WHITELIST)
        )
        self.timeout = timeout or getattr(settings, 'COMMAND_TIMEOUT', DEFAULT_TIMEOUT)
        self._commands = None

    @property
    def commands(self):
        """惰性查询命令表，避免模块导入阶段访问数据库。"""
        if self._commands is None:
            self._commands = list(commands.objects.all())
        return self._commands

    def refresh(self):
        """丢弃缓存并重新读取命令表，供后台修改命令后立即生效。"""
        self._commands = None
        return self.commands

    def _find(self, title):
        """按标题查找命令记录，标题比较不区分大小写。"""
        if not title:
            return None
        target = str(title).upper()
        for command in self.commands:
            if command.title.upper() == target:
                return command
        return None

    def run(self, title):
        """执行指定标题对应的命令。

        :param title: 命令标题
        :return: 命令输出或提示信息
        """
        command = self._find(title)
        if command is None:
            return '未找到相关命令，请输入hepme获得帮助。'
        return self.execute(command.command)

    @staticmethod
    def _parse(command):
        """把命令串拆成参数列表，拆分失败返回空列表。"""
        if not command or not str(command).strip():
            return []
        try:
            return shlex.split(str(command))
        except ValueError as exc:
            logger.warning('命令解析失败：%s', exc)
            return []

    def execute(self, command):
        """校验并执行一条命令。

        :param command: 待执行的命令串
        :return: 合并了标准输出与标准错误的结果文本
        """
        parts = self._parse(command)
        if not parts:
            return '命令为空或格式不正确'
        if not self.is_allowed(parts[0]):
            return '命令不在允许列表中：%s' % parts[0]
        try:
            completed = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            return '命令执行超时（超过 %s 秒）' % self.timeout
        except FileNotFoundError:
            return '命令不存在：%s' % parts[0]
        except PermissionError:
            return '没有权限执行命令：%s' % parts[0]
        except Exception as exc:
            logger.error('命令执行异常：%s', exc)
            return '命令执行出错!'
        output = ((completed.stdout or '') + (completed.stderr or '')).strip()
        if not output:
            return '命令已执行，无输出'
        if len(output) > MAX_OUTPUT_LENGTH:
            output = output[:MAX_OUTPUT_LENGTH] + '\n……（输出已截断）'
        return output

    def is_allowed(self, name):
        """判断命令名是否在白名单内。"""
        return str(name) in self.whitelist

    def get_help(self):
        """拼接全部命令的标题与说明，供帮助信息展示。"""
        return ''.join(
            '{c}:{d}\n'.format(c=command.title, d=command.describe)
            for command in self.commands
        )


if __name__ == '__main__':
    chatbot = ChatGPT()
    print(chatbot.ask("写一篇1000字关于AI的论文"))
