#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: forms.py.py
@Time: 2020/4/11 19:26
'''
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'gender')
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        #     'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent', 'rows': 40, 'cols': 60}),
        # }

