#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: urls.py.py
@Time: 2020/4/11 22:11
'''
from django.conf.urls import url
from django.contrib.auth.views import LoginView, PasswordResetView

from . import views

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', views.MyLogoutView.as_view(), name='logout'),

    url(r'^my_zone/(?P<pk>\w+)/$', views.PersonalInfoDetailView.as_view(), name='my_zone'),
    url(r'^my_zone/(?P<pk>\w+)/edit/$', views.UpdatePersonalInfoView.as_view(), name='update_personal_info'),
    url(r'^my_zone/(?P<pk>\w+)/preference/$', views.update_preference_setting, name='update_preference'),
    url(r'^subscribe/(?P<pk>\d+)/$', views.subscribe, name='subscribe'),
    url(r'^registration/new/$', views.user_register, name='new_user'),
    url(r'^registration/activate/(?P<token>\w+)/$', views.activate_user_account, name='activate_user'),
    url(r'^registration/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^registration/password/reset/done/$', views.reset_password_done, name='password_reset_done'),
]
