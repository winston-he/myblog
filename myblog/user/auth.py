#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: auth.py
# @Time: 2020-06-17 16:09
# @Email: winston.wz.he@gmail.com
# @Desc:
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
