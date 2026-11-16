"""运维助手视图。

cgw: 第9-10周新增。为管理员提供一个可操作的运维入口，包含"执行已登记
命令""直接执行命令""AI 问答"三个区块，同时作为命令白名单校验与大模型
接口修复的验证界面。
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from servermanager.api.commonapi import ChatGPT, CommandHandler
from servermanager.forms import ChatForm, ExistingCommandForm, FreeCommandForm


# cgw: 三个表单动作的常量，避免在视图里散落魔法字符串
ACTION_REGISTERED = 'registered'
ACTION_FREE = 'free'
ACTION_CHAT = 'chat'


def _command_choices(handler):
    """把命令表转换成下拉框选项。"""
    return [
        (command.title, '%s：%s' % (command.title, command.describe))
        for command in handler.commands
    ]


@login_required
def console(request):
    """运维助手页面。

    仅允许 is_staff 用户访问；未登录由 ``login_required`` 跳转登录页，
    已登录但无管理权限返回 403。
    """
    if not request.user.is_staff:
        raise PermissionDenied('仅管理员可访问运维助手')

    handler = CommandHandler()
    choices = _command_choices(handler)

    registered_form = ExistingCommandForm(choices=choices)
    free_form = FreeCommandForm()
    chat_form = ChatForm()

    command_result = ''
    chat_answer = ''
    result_source = ''
    error_message = ''

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == ACTION_REGISTERED:
            registered_form = ExistingCommandForm(request.POST, choices=choices)
            if registered_form.is_valid():
                title = registered_form.cleaned_data.get('title')
                if not title:
                    error_message = '请选择一条已登记的命令'
                else:
                    command_result = handler.run(title)
                    result_source = '已登记命令：%s' % title

        elif action == ACTION_FREE:
            free_form = FreeCommandForm(request.POST)
            if free_form.is_valid():
                command = free_form.cleaned_data['command']
                command_result = handler.execute(command)
                result_source = '直接执行：%s' % command
            else:
                error_message = '命令输入不合法'

        elif action == ACTION_CHAT:
            chat_form = ChatForm(request.POST)
            if chat_form.is_valid():
                prompt = chat_form.cleaned_data['prompt']
                chatbot = ChatGPT()
                chat_answer = chatbot.ask(prompt)
                if not chatbot.is_configured():
                    error_message = '尚未配置 OPENAI_API_KEY，AI 问答不可用'
            else:
                error_message = '问题输入不合法'
        else:
            error_message = '未知的操作类型'

    context = {
        'registered_form': registered_form,
        'free_form': free_form,
        'chat_form': chat_form,
        'command_result': command_result,
        'chat_answer': chat_answer,
        'result_source': result_source,
        'error_message': error_message,
        'command_count': len(choices),
        'whitelist': handler.whitelist,
    }
    return render(request, 'servermanager/console.html', context)
