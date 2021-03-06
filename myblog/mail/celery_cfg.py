#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: celery_cfg.py
@Time: 2020/6/21 1:05
'''

BACKEND_HOST = '123.57.201.57'
BROKER_HOST = '123.57.201.57'

class Config:
    result_backend = 'db+mysql://winston:Hwzhen123.@{}/async_tasks'.format(BACKEND_HOST)
    broker_url = 'amqp://openstack:123456@{}:5672/'.format(BROKER_HOST)