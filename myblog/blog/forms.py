#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: forms.py
# @Time: 2020-03-04 15:42
# @Email: winston.wz.he@gmail.com
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    publish = forms.CharField(required=False)
    draft = forms.CharField(required=False)

    def clean(self):
        """
        使用publish 和 draft两个字段判断是发布还是存为草稿，在这里作处理
        :return:
        """
        if 'publish' not in self.cleaned_data or 'draft' not in self.cleaned_data:
            raise forms.ValidationError("Critical error occurs")
        publish = self.cleaned_data['publish']
        draft = self.cleaned_data['draft']

        if publish != '' and draft == '':
            self.cleaned_data['is_publish'] = True
        elif publish == '' and draft != '':
            self.cleaned_data['is_publish'] = False
        else:
            raise forms.ValidationError("Critical error occurs")

        del self.cleaned_data['publish']
        del self.cleaned_data['draft']
        return super().clean()

    class Meta:
        model = Post
        fields = ('title', 'content', 'publish', 'draft')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content': forms.Textarea(
                attrs={'class': 'editable medium-editor-textarea postcontent', 'rows': 40, 'cols': 60}),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea', 'rows': 4, 'cols': 80}),
        }


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
