#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: urls.py
# @Time: 2020-03-04 15:40
# @Email: winston.wz.he@gmail.com
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^post', name='post_detail'),
    url(name='draft_list'),
    url(name='post_create'),
    url(name='post_update'),
    url(name='post_remove'),
    url(name='comment_create'),
    url(name='comment_remove'),
]