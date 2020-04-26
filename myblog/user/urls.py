#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: urls.py.py
@Time: 2020/4/11 22:11
'''
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/new$', views.CreateUserView.as_view(), name='new_user')
]