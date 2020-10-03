#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: urls.py
# @Time: 2020-03-04 15:40
# @Email: winston.wz.he@gmail.com
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^about/$', views.AboutView.as_view(), name='about')
    url(r'^post_list/$', views.PostListView.as_view(), name='post_list'),
    # url(r'^drafts/$', views.MyPostListView.as_view(), name='my_post_list'),
    url(r'^post/marked/$', views.MarkedPostListView.as_view(), name='marked_post_list'),
    url(r'^post/(?P<pk>\d+)/detail/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'post/uploadimage/$', views.upload_image, name='upload_image'),

    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.UpdatePostView.as_view(), name='post_publish'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.UpdatePostView.as_view(), name='post_update'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.DeletePostView.as_view(), name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.CreateCommentView.as_view(), name='comment_new'),

    url(r'^post/(?P<pk>\d+)/comment/count$', views.PostDetailView.get_total_comment_count, name='comment_count'),
    url(r'^comment/(?P<pk>\d+)/delete/$', views.DeleteCommentView.as_view(), name='comment_remove'),
    url(r'^post/(?P<pk>\d+)/comment-list/$', views.CommentListView.as_view(), name='comment_list'),
    url(r'^post/(?P<pk>\d+)/like/$', views.like_post, name='like_post'),
    url(r'^post/(?P<pk>\d+)/mark/$', views.mark_post, name='mark_post'),
    url(r'^comment/(?P<pk>\d+)/like/$', views.like_comment, name='like_comment'),
    url(r'^comment/(?P<pk>\d+)/dislike/$', views.dislike_comment, name='dislike_comment'),
    url(r'^my_comments/$', views.MyCommentList.as_view(), name='my_comments'),

    url(r'^my_subscribes/$', views.SubscribeListView.as_view(), name='my_subscribes'),

    url(r'^personal_stats/$', views.personal_summary, name='personal_stats'),
    url(r'^post/(?P<pk>\d+)/view/$', views.increase_view_count, name='view_count'),

    # 举报违规内容
    url(r'^report/(?P<type>\d+)/(?P<pk>\d+)/$', views.ReportViolationView.as_view(), name='report_violation'),
]
