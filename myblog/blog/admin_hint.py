#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: admin_hint.py
@Time: 2020/10/5 17:04
'''
from datetime import datetime

from jinja2 import Template

"""
对管理员进行审核的相关提示
"""
import MySQLdb

from celery import Celery
from celery.schedules import crontab
import jinja2
app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/10"),
                             send_hint_message.s())

@app.task
def send_hint_message():
    conn = MySQLdb.connect(
        host='123.57.201.57',
        port=3306,
        user='winston',
        passwd='Hwzhen123.',
        db='myblog'
    )
    with conn.cursor() as cursor:
        # 查找需要审核的博客
        conn.set_character_set('gbk')
        cursor.execute("select username, published_time, title  from blog_post b inner join auth_user a on"
                       " b.author_id=a.id where status=1;")

        blog_to_approve = cursor.fetchall()

        # 查找被举报的博客和评论
        cursor.execute("select * from (select p.title content, b.create_time, b.comment, a.username post_by, related_object_type from blog_violationreport b inner join auth_user a on b.post_by_id=a.id "
                       "inner join blog_post p on b.related_object=p.id where b.related_object_type=0 "
                       "union "
                       "select p.content content, b.create_time, b.comment, a.username post_by, related_object_type from blog_violationreport b inner join auth_user a on b.post_by_id=a.id "
                       "inner join blog_comment p on b.related_object=p.id where b.related_object_type=1) x order by related_object_type desc;")
        violation_items = cursor.fetchall()

        # 如果没有结果
        if len(blog_to_approve) == 0 and len(violation_items) == 0:
            return

        env = jinja2.Environment(loader=jinja2.FileSystemLoader("D:\PyCharm_Project\myblog\myblog\myblog\\templates\mail"))
        t = env.get_template('hint_message.html')
        res = t.render({
            'time': datetime.now(),
            'blog_to_approve': blog_to_approve,
            'violation_items': {
                "blogs": tuple(filter(lambda x: x[-1]==0, violation_items)),
                "comments": tuple(filter(lambda x: x[-1]==1, violation_items)),
            }
        })

        # send_email()
#
# send_hint_message()