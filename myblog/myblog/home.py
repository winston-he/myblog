#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: home.py
@Time: 2020/8/1 23:10
'''
from django.shortcuts import render, redirect
from django.urls import reverse


def home(request):
    return render(request, template_name="blog/post_list.html")
    # return redirect(reverse('post_list', kwargs={"page": 1}))