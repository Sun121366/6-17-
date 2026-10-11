# [TWL/唐文龙] 本文件中 2026-10-07 新增的中文模型说明、配置说明与业务注释由唐文龙补充整理。
# Create your models here.
# [TWL/唐文龙] 以下模块说明由本人补充。
"""第三方登录相关模型。

OAuthUser 保存第三方平台返回的用户身份，并可绑定到站内 BlogUser；
OAuthConfig 保存各 OAuth 平台的客户端配置。
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class OAuthUser(models.Model):
    # [TWL/唐文龙] 以下模型说明由本人补充。
    """第三方用户映射模型。

    author 为空时表示第三方身份尚未绑定站内账号；绑定后一个站内用户可以
    关联多个不同平台的 OAuthUser 记录。
    """
    # 绑定的站内用户；允许为空，表示第三方账号暂未完成绑定。 [TWL]
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    openid = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, verbose_name=_('nick name'))
    token = models.CharField(max_length=150, null=True, blank=True)
    picture = models.CharField(max_length=350, blank=True, null=True)
    type = models.CharField(blank=False, null=False, max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = _('oauth user')
        verbose_name_plural = verbose_name
        ordering = ['-creation_time']


class OAuthConfig(models.Model):
    # [TWL/唐文龙] 以下模型说明由本人补充。
    """OAuth 平台配置模型。

    保存平台类型、AppKey、AppSecret 和回调地址；同一平台只允许存在一条配置。
    """
    TYPE = (
        ('weibo', _('weibo')),
        ('google', _('google')),
        ('github', 'GitHub'),
        ('facebook', 'FaceBook'),
        ('qq', 'QQ'),
    )
    # 平台类型，例如 weibo、github、google、qq。 [TWL]
    type = models.CharField(_('type'), max_length=10, choices=TYPE, default='a')
    appkey = models.CharField(max_length=200, verbose_name='AppKey')
    appsecret = models.CharField(max_length=200, verbose_name='AppSecret')
    callback_url = models.CharField(
        max_length=200,
        verbose_name=_('callback url'),
        blank=False,
        default='')
    is_enable = models.BooleanField(
        _('is enable'), default=True, blank=False, null=False)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)

    def clean(self):
        if OAuthConfig.objects.filter(
                type=self.type).exclude(id=self.id).count():
            raise ValidationError(_(self.type + _('already exists')))

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'oauth配置'
        verbose_name_plural = verbose_name
        ordering = ['-creation_time']
