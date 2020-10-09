# coding: utf-8
# @Author: Winston He
# @Email: winston.wz.he@gmail.com
# @Date: 2020/10/3 22:20
# @File: urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^about/$', views.AboutView.as_view(), name='about')
    url(r'^intro/$', views.IntroductionView.as_view(), name='introduction'),
]