#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: urls.py
# @Time: 2020-08-25 14:05
# @Email: winston.wz.he@gmail.com
# @Desc:
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^chat/$', views.ChatRoomView.as_view(), name='chat'),
    url(r'^chat/info', views.webim_info, name='webim_info'),
    url(r'^chat_record_list/$', views.ChatListView.as_view(), name='chat_record_list'),
    url(r'^chat/signature', views.update_signature, name='update_signature'),
]
