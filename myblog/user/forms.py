#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: forms.py.py
@Time: 2020/4/11 19:26
'''
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import IntegerField, RadioSelect

from .models import UserProfile


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'gender']
        widgets = {
            'gender': RadioSelect()
        }

    gender = IntegerField(min_value=0, max_value=2)
