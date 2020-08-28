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
    val = val.replace("days", "天")
    val = val.replace("day", "天")
    val = val.replace("hours", "小时")
    val = val.replace("hour", "小时")
    val = val.replace("months", "个月")
    val = val.replace("month", "个月")
    val = val.replace("years", "年")
    return val.replace("year", "年")


@register.filter
def md_to_html(md_string: str):
    return markdown.markdown(md_string)