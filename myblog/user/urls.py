#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: urls.py.py
@Time: 2020/4/11 22:11
'''
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView

from . import views
from .views import PasswordReset, PasswordResetConfirm, MyLoginView

urlpatterns = [
    url(r'^login/$', MyLoginView.as_view(), name='login'),
    url(r'^logout/$', views.MyLogoutView.as_view(), name='logout'),

    url(r'^my_zone/(?P<pk>\d+)/$', views.PersonalInfoDetailView.as_view(), name='my_zone'),
    url(r'^my_zone/(?P<pk>\d+)/edit/$', views.UpdatePersonalInfoView.as_view(), name='update_personal_info'),

    url(r'^my_zone/profile_image/$', views.ProfileImageView.as_view(), name='profile_image'),
    url(r'^my_zone/(?P<pk>\d+)/preference/$', views.update_preference_setting, name='update_preference'),
    url(r'^subscribe/(?P<pk>\d+)/$', views.subscribe, name='subscribe'),
    url(r'^registration/new/$', views.user_register, name='new_user'),
    url(r'^registration/activate/(?P<token>.+)$', views.activate_user_account, name='activate_user'),
    url(r'^registration/password/reset/$', PasswordReset.as_view(), name='reset_password'),
    url(r'^registration/password/reset/(?P<token>.+)$', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^registration/password/reset/done/$', views.reset_password_done, name='password_reset_done'),
]
