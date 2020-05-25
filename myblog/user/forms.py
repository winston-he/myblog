#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: forms.py.py
@Time: 2020/4/11 19:26
'''
# from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.forms import ModelForm, Textarea, TextInput, PasswordInput, EmailInput, RadioSelect, CharField

from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'email', 'gender']
        widgets = {
            'name': TextInput(),
            'password': PasswordInput(),
            'email': EmailInput(),
            'gender': RadioSelect()
        }

    def clean(self):
        pass

    password_confirm = CharField(required=True, max_length=32, min_length=6, error_messages="")


