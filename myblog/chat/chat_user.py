#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: chat_user.py
@Time: 2020/9/24 16:40
'''
import requests
from django.core.cache import cache
from django_redis import get_redis_connection

from .decorators import webim_token_check
from . import *

REQUEST_PREFIX = WEBIM_REQUEST_HOST + '/' + ORG_NAME + '/' + APP_NAME

@webim_token_check
def create_chat_user(username: str, password: str):
    conn = get_redis_connection("default")
    token = conn.hget("webim_info", "token")
    resp = requests.post('{}/{}/{}/users'.format(WEBIM_REQUEST_HOST, ORG_NAME, APP_NAME), json={
        "username": username,
        "password": password
    }, **{
        "headers": {
            "authorization": "Bearer " + token
        }
    })

    assert resp.status_code == 200

@webim_token_check
def add_chat_user(owner, friend, token):
    requests.post('{}/users/{}/contact/users/{}'.format(REQUEST_PREFIX, owner, friend),
                  headers={"authorization": "Bearer " + token})

@webim_token_check
def get_friend_list(user):
    pass