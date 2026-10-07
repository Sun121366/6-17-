"""服务器管理辅助模型。

保存运维命令说明和邮件发送日志，供后台管理及问题排查使用。
"""

from django.db import models


# Create your models here.
class commands(models.Model):
    """运维命令说明模型。

    类名保持项目原有命名，避免改变既有迁移和数据库表名；记录命令标题、
    实际命令、用途说明及创建/修改时间。
    """
    title = models.CharField('命令标题', max_length=300)
    command = models.CharField('命令', max_length=2000)
    describe = models.CharField('命令描述', max_length=300)
    creation_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '命令'
        verbose_name_plural = verbose_name


class EmailSendLog(models.Model):
    """邮件发送日志模型。

    记录收件人、标题、正文和发送结果，用于追踪系统通知是否成功。
    """
    emailto = models.CharField('收件人', max_length=300)
    title = models.CharField('邮件标题', max_length=2000)
    content = models.TextField('邮件内容')
    send_result = models.BooleanField('结果', default=False)
    creation_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '邮件发送log'
        verbose_name_plural = verbose_name
        ordering = ['-creation_time']
