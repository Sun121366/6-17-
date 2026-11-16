# cgw: 第9-10周新增运维助手路由；微信机器人回调路径保持不变。
from django.urls import path
from werobot.contrib.django import make_view

from . import views
from .robot import robot

app_name = "servermanager"
urlpatterns = [
    path(r'robot', make_view(robot)),
    path(r'servermanager/console/', views.console, name='console'),
]
