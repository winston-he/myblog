#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: middleware.py
# @Time: 2020-08-28 10:55
# @Email: winston.wz.he@gmail.com
# @Desc:
from . models import AccessLog

class AccessLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # 分发URL之前

        AccessLog(request_user=request.META.get("USER"),
                  request_path=request.META.get("PATH_INFO"),
                  request_method=request.META.get("REQUEST_METHOD"),
                  remote_addr=request.META.get("REMOTE_ADDR"),
                  host_addr=request.META.get("HTTP_HOST")).save()
        response = self.get_response(request)


        return response

