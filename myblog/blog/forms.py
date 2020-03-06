#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: forms.py
# @Time: 2020-03-04 15:42
# @Email: winston.wz.he@gmail.com
from django import forms
from .models import Post, Comment
from bootstrap_modal_forms.mixins import PopRequestMixin

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }



class CommentForm(forms.ModelForm, PopRequestMixin):
    class Meta:
        model = Comment
        fields = ('content', )
        # widgets = {
        #     'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        # }

