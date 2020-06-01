#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: urls.py
# @Time: 2020-06-01 15:04
# @Email: winston.wz.he@gmail.com
# @Desc:
from django.conf.urls import url

from chat import views

urlpatterns = [
    url(r'^chat/$', views.index, name='index'),
    url(r'^chat/(?P<room_name>\w+)/', views.room, name='room')
]

