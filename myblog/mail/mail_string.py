#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: mail_string.py
@Time: 2020/5/3 16:13
'''


def get_activate_msg(username, link):
    return '<!DOCTYPE html>' \
           '<html lang="en" dir="ltr">' \
           '<head>' \
           '<meta charset="utf-8">' \
           '<title>Myblog邮箱激活通知</title>' \
           '</head>' \
           '<body>' \
           '<h1>尊敬的用户： {username}, 请在24小时内点击以下链接以完成验证（如果超时，须重新注册）：{link}' \
           '</h1></body>' \
           '</html>'.format(username=username, link=link)

