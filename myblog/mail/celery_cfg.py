#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: celery_cfg.py
@Time: 2020/6/21 1:05
'''

BACKEND_HOST = '123.57.201.57'

class Config:
    result_backend = 'db+mysql://winston:wins1603@{}/myblog'.format(BACKEND_HOST)
