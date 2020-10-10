#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: blog_filter.py
@Time: 2020/8/16 21:48
'''
from datetime import datetime, timedelta

from django import template
import codecs, markdown

register = template.Library()

@register.filter
def timesince_zh(val: str):
    return val


@register.filter
def md_to_html(md_string: str):
    return markdown.markdown(md_string)