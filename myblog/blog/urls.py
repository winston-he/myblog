#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: urls.py
# @Time: 2020-03-04 15:40
# @Email: winston.wz.he@gmail.com
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^drafts/$', views.MyPostListView.as_view(), name='my_post_list'),
    url(r'^post/marked/$', views.MarkedPostListView.as_view(), name='marked_post_list'),
    url(r'^post/(?P<pk>\d+)/detail/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.save_post, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.UpdatePostView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.CreatePostView.publish_post, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.delete_post, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.CreateCommentView.save, name='comment_new'),
    url(r'^comment/(?P<pk>\d+)/delete/$', views.remove_comment, name='comment_remove'),
    url(r'^comment/$', views.CommentListView.as_view(), name='comment_list'),
    url(r'^post/(?P<pk>\d+)/like/$', views.like_post, name='like_post'),
    url(r'^post/(?P<pk>\d+)/mark/$', views.mark_post, name='mark_post'),
    url(r'^comment/(?P<pk>\d+)/like/$', views.like_comment, name='like_comment'),
    url(r'^comment/(?P<pk>\d+)/dislike/$', views.dislike_comment, name='dislike_comment'),
    url(r'^post/(?P<pk>\d+)/view/$', views.add_view_count, name='view_count')
]


