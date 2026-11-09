# szj: ===== comments 应用 · 表单定义（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: CommentForm 只暴露“评论正文”一个可见字段；parent_comment_id 作为隐藏字段
# szj: 传递父评论主键，用来实现“回复某条评论”的嵌套评论功能。
"""评论提交表单。

表单字段刻意保持最小：正文由用户在页面输入，父评论 ID 由前端以隐藏域提交，
其余字段（作者、文章、审核状态）全部由视图在服务端补齐，避免被客户端篡改。
"""

from django import forms
from django.forms import ModelForm

from .models import Comment


class CommentForm(ModelForm):
    """发表评论/回复评论的表单。

    - ``body``：评论正文，来自 Comment.body；
    - ``parent_comment_id``：隐藏字段，回复时携带父评论主键，顶层评论时为空。
    """

    # szj: 隐藏字段 + required=False：顶层评论不需要父评论，回复时由页面 JS 填入父评论文本。
    parent_comment_id = forms.IntegerField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        """限定可提交字段，防止客户端越权提交 author/article 等敏感字段。"""

        model = Comment
        fields = ['body']
