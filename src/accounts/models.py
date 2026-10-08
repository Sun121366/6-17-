# [TWL/唐文龙] 本文件中 2026-10-07 新增的中文模型说明、配置说明与业务注释由唐文龙补充整理。
"""用户与账号模型。

该模块定义博客系统的统一用户模型，并通过 Django 的认证框架提供
登录、权限、用户资料和作者主页所需的数据结构。
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from djangoblog.utils import get_current_site


# Create your models here.

class BlogUser(AbstractUser):
    """博客用户模型。

    继承 Django 的 AbstractUser，复用用户名、密码、邮箱、权限和登录能力；
    在此基础上扩展博客业务需要的昵称、创建时间、修改时间和来源字段。
    项目通过 AUTH_USER_MODEL 将其作为统一用户模型使用。
    """
    # 页面展示优先使用昵称；为空时可回退到 username。 [TWL]
    nickname = models.CharField(_('nick name'), max_length=100, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    source = models.CharField(_('create source'), max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse(
            'blog:author_detail', kwargs={
                'author_name': self.username})

    def __str__(self):
        return self.email

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'
