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
    url(r'^post/(?P<pk>\d+)/detail/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.save, name='post_new'),
    # url(r'^draft/$', views.DraftListView.as_view(), name='draft_list'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.UpdatePostView.as_view(), name='post_edit'),
    # url(r'^post/(?P<pk>\d+)/publish/$', views.CreatePostView.publish, name='post_publish'),
    # url(r'^post/(?P<pk>\d+)/delete/$', views.DeletePostView.as_view(), name='post_remove'),
    # url(r'^comment/new/$', views.CreatePostView.as_view(), name='comment_create'),
    # url(r'^comment/(?P<pk>\d+)/delete/$', views.DeleteCommentView.as_view(), name='comment_remove'),
]

# urlpatterns = [
#     url(r'^$', views.PostListView.as_view(), name='post_list'),
#     url(r'^about/$', views.AboutView.as_view(), name='about'),
#     url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
#     url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
#     url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
#     url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),
#     url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
#     url(r'^post/(?P<pk>\d+)/publish/$', views.CreatePostView.post_publish, name='post_publish'),
#     url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
#     url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
#     url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
# ]
