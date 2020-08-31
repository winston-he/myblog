#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: routing.py
# @Time: 2020-08-25 14:40
# @Email: winston.wz.he@gmail.com
# @Desc:
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]