#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: marsh.py
# @Time: 2020-08-04 16:26
# @Email: winston.wz.he@gmail.com
# @Desc:
from marshmallow import Schema, fields


class BlogPostPreviewSchema(Schema):
    id = fields.Integer()
    author = fields.String()
    published_time = fields.DateTime(format="%Y/%m/%d $H:%M:%S")
    create_time = fields.DateTime(format="%Y/%m/%d $H:%M:%S")
    title = fields.String()
    content = fields.Field()
    liked_count = fields.Integer()
    marked_count = fields.Integer()
    comment_count = fields.Integer()
    viewed_count = fields.Integer()

class BlogCommentDetailSchema(Schema):
    pass

