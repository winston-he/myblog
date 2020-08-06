#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: forms.py.py
@Time: 2020/4/11 19:26
'''
from django.contrib.auth.models import User
from django.forms import IntegerField, RadioSelect, CharField, EmailField
from django import forms

from .models import UserProfile


class UserRegisterForm(forms.Form):
    username = CharField(max_length=50, min_length=10, required=True, error_messages={"username": "用户名长度介于10到50之间"})
    password1 = CharField(max_length=25, min_length=8, required=True, error_messages={"password1": "密码长度介于8到25之间"})
    password2 = CharField(max_length=25, min_length=8, required=True, error_messages={"password2": "密码长度介于8到25之间"})
    email = EmailField(error_messages={"email": "请输入合法的邮箱"})

    def clean(self):
        if super().is_valid():
            cleaned_data = super(UserRegisterForm, self).clean()

            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError({"password1": "两次输入的密码不一致！"})
            self.cleaned_data['password'] = self.cleaned_data['password1']
            del self.cleaned_data['password1']
            del self.cleaned_data['password2']





