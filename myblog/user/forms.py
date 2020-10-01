#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: forms.py
@Time: 2020/4/11 19:26
'''
from django.contrib.auth.models import User
from django.forms import IntegerField, RadioSelect, CharField, EmailField
from django import forms
from .models import ACADEMY_LIMITS, EMPLOYMENT_LIMITS
from .models import UserProfile


class PasswordResetForm(forms.Form):
    password1 = CharField(max_length=25, min_length=8, required=True, error_messages={"password1": "密码长度介于8到25之间"})
    password2 = CharField(max_length=25, min_length=8, required=True, error_messages={"password2": "密码长度介于8到25之间"})

    def clean(self):
        if super().is_valid():
            cleaned_data = super(PasswordResetForm, self).clean()

            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError({"password1": "两次输入的密码不一致！"})
            self.cleaned_data['password'] = self.cleaned_data['password1']
            del self.cleaned_data['password1']
            del self.cleaned_data['password2']

# 用户注册使用的表单
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

class PersonalInfoForm(forms.ModelForm):
    nickname = forms.CharField(required=True, max_length=64)
    introduction = forms.CharField(max_length=300, required=False)
    location1 = forms.CharField(max_length=100, required=False)
    location2 = forms.CharField(max_length=100, required=False)
    location3 = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     for i in range(1, ACADEMY_LIMITS+1):
    #         edu_school = 'edu_school_' + str(i)
    #         edu_major = 'edu_major_' + str(i)
    #         start_date = 'edu_start_date_' + str(i)
    #         end_date = 'edu_end_date_' + str(i)
    #         try:
    #             self.fields[edu_school] = forms.CharField(max_length=50, required=True)
    #             self.fields[edu_major] = forms.CharField(max_length=50, required=True)
    #             self.fields[start_date] = forms.CharField(max_length=50, required=True)
    #             self.fields[end_date] = forms.CharField(max_length=50)
    #         except KeyError:
    #             break
    #
    #     for i in range(1, EMPLOYMENT_LIMITS+1):
    #         company = 'company_' + str(i)
    #         title = 'edu_major_' + str(i)
    #         start_date = 'emp_start_date_' + str(i)
    #         end_date = 'emp_end_date_' + str(i)
    #         try:
    #             self.fields[company] = forms.CharField(max_length=50, required=True)
    #             self.fields[title] = forms.CharField(max_length=50, required=True)
    #             self.fields[start_date] = forms.CharField(max_length=50, required=True)
    #             self.fields[end_date] = forms.CharField(max_length=50)
    #         except KeyError:
    #             break

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


