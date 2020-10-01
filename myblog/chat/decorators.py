#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: decorators.py
@Time: 2020/9/24 14:20
'''
import json
import os
from functools import wraps
import requests
from django.core.cache import cache
from django_redis import get_redis_connection
from . import *

"""
检查token的状态是否过期，如果过期则更新
"""
def webim_token_check(func):
    @wraps(func)
    def wrapped(*args, **kwargs):

        conn = get_redis_connection("default")

        token = conn.hget("webim_info", 'token')

        # 发送一个请求，测试token是否过期
        resp = requests.get('{}/{}/{}/users?limit=1'.format(WEBIM_REQUEST_HOST, ORG_NAME, APP_NAME), params={
            "headers": {
                "authorization": "Bearer " + token if token else ''
            }
        })
        # 过期或未授权
        if resp.status_code == 401:
            resp = requests.post(
                '{}/{}/{}/token'.format(WEBIM_REQUEST_HOST, ORG_NAME, APP_NAME),
                json={
                  "grant_type": "client_credentials",
                  "client_id": CLIENT_ID,
                  "client_secret": CLIENT_SECRET
                }
            )
            token = json.loads(resp.text)['access_token']
            conn.hset('webim_info', 'token', token)
        kwargs['token'] = token
        return func(*args, **kwargs)
    return wrapped
