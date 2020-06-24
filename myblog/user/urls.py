#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: urls.py.py
@Time: 2020/4/11 22:11
'''
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from . import views

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^user/new/$', views.UserRegisterView.as_view(), name='new_user'),
    url(r'^user/activate/(?P<token>\w+)/$', views.activate_user_account, name='activate_user'),
    url(r'^user/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^user/password/reset/done/$', views.reset_password_done, name='password_reset_done'),
]