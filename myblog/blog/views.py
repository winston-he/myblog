from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.
class AboutView(TemplateView):
    template_name = ''


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_time__isnul=False).order_by('-published_time')


class DraftListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_time__isnul=True).order_by('-create_time')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'
    model = Post
    form_class = PostForm

    @staticmethod
    def publish(pk):
        Post.objects.filter(pk=pk).update()


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'
    model = Post
    form_class = PostForm


class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = reverse('post_list')


class CreateCommentView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'
    model = Comment
    form_class = CommentForm


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = reverse('post_detail')
