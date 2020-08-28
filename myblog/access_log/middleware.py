#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: middleware.py
# @Time: 2020-08-28 10:55
# @Email: winston.wz.he@gmail.com
# @Desc:


class AccessLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # 分发URL之前
        response = self.get_response(request)


        return response

    # 视图函数执行前
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    # 发生异常
    def process_exception(self, request, exception):
        pass

    # 视图函数执行完毕，渲染视图之前
    def process_template_response(request, response):
        pass

