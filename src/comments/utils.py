# szj: ===== comments 应用 · 邮件通知工具（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 本模块只有一个入口 send_comment_email，负责两类评论通知：
# szj:   1) 评论保存成功后，向评论者本人发送“感谢评论”邮件并附文章回链；
# szj:   2) 若该评论是回复，再向被回复者发送“收到回复”提醒邮件。
# szj: 本次质量改进：修复行尾空格与超长行、统一 f-string、异常捕获改为 logger.exception
# szj: 记录完整堆栈，并明确邮件发送失败不应影响评论主流程。
"""评论邮件通知工具。

评论落库成功后由业务层调用本模块，异步地（同步调用但不阻塞失败）
向相关用户发送邮件通知。任何邮件异常都只记录日志，不向上抛出。
"""

import logging

from django.utils.translation import gettext_lazy as _

from djangoblog.utils import get_current_site, send_email

logger = logging.getLogger(__name__)


def _build_article_url(comment):
    """拼出评论所属文章的完整外链地址。

    :param comment: 评论对象
    :return: 形如 ``https://<站点域名>/article/...`` 的绝对地址
    """
    site = get_current_site().domain
    return f"https://{site}{comment.article.get_absolute_url()}"


def send_comment_email(comment):
    """发送评论相关的邮件通知。

    只对“评论成功”这一业务结果负责：先给评论作者发送感谢邮件；
    如果该评论是回复，再给父评论作者发送回复提醒。

    :param comment: 已保存的评论对象，需已关联 article 与 author
    """
    article_url = _build_article_url(comment)
    subject = _('Thanks for your comment')

    # szj: 通知一：向评论者本人发送感谢信，附文章链接方便其回看自己的评论。
    thanks_mail_content = _(
        """<p>Thank you very much for your comments on this site</p>
                    You can visit <a href="%(article_url)s" rel="bookmark">%(article_title)s</a>
                    to review your comments,
                    Thank you again!
                    <br />
                    If the link above cannot be opened, please copy this link to your browser.
                    %(article_url)s"""
    ) % {
        'article_url': article_url,
        'article_title': comment.article.title,
    }
    try:
        send_email([comment.author.email], subject, thanks_mail_content)

        # szj: 通知二：仅当存在父评论时，才通知被回复者“你的评论收到了回复”。
        if comment.parent_comment:
            reply_mail_content = _(
                'Your comment on <a href="%(article_url)s" rel="bookmark">'
                '%(article_title)s</a><br/> has received a reply. <br/> %(comment_body)s'
                ' <br/> go check it out!'
                ' <br/> If the link above cannot be opened, please copy this link to your browser.'
                ' %(article_url)s'
            ) % {
                'article_url': article_url,
                'article_title': comment.article.title,
                'comment_body': comment.parent_comment.body,
            }
            send_email(
                [comment.parent_comment.author.email], subject, reply_mail_content)
    except Exception:  # pylint: disable=broad-exception-caught
        # szj: 邮件服务属于外部依赖，失败时只记录堆栈（exc_info=True），不影响已保存的评论。
        logger.exception('发送评论邮件通知失败: comment_id=%s', comment.pk)
