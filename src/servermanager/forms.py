"""运维助手页面的表单定义。

cgw: 本文件为第9-10周新增。三个表单分别对应"执行已有命令""直接执行命令"
"AI 问答"三个入口，命令输入统一走白名单校验，不做任何拼接执行。
"""

from django import forms

# cgw: 统一输入框样式，与前台 Tailwind 视觉保持一致
INPUT_CLASS = (
    'w-full rounded-lg border border-border bg-background px-3 py-2 text-sm '
    'text-foreground focus:border-primary focus:outline-none'
)


class ExistingCommandForm(forms.Form):
    """从命令表中选择一条已登记的命令执行。"""

    title = forms.ChoiceField(label='命令', choices=(), required=False)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', ())
        super().__init__(*args, **kwargs)
        self.fields['title'].choices = [('', '请选择已登记的命令')] + list(choices)
        self.fields['title'].widget.attrs.update({'class': INPUT_CLASS})

    def clean_title(self):
        """空选择视为未选择，交由视图给出提示。"""
        return self.cleaned_data.get('title', '').strip()


class FreeCommandForm(forms.Form):
    """直接输入命令串执行，仅允许白名单内的命令。"""

    command = forms.CharField(
        label='命令',
        max_length=500,
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '例如 ls -al'}),
    )

    def clean_command(self):
        """去掉首尾空白，拒绝空命令。"""
        command = (self.cleaned_data.get('command') or '').strip()
        if not command:
            raise forms.ValidationError('请输入要执行的命令')
        return command


class ChatForm(forms.Form):
    """向大模型提问。"""

    prompt = forms.CharField(
        label='问题',
        max_length=1000,
        widget=forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': '向 AI 提问'}),
    )

    def clean_prompt(self):
        """去掉首尾空白，拒绝空问题。"""
        prompt = (self.cleaned_data.get('prompt') or '').strip()
        if not prompt:
            raise forms.ValidationError('请输入问题内容')
        return prompt
