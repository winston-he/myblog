from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm, PostForm
from .models import Post, Comment


# Create your views here.
# class AboutView(TemplateView):
#     template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_time__isnull=False).order_by('-published_time')


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-published_time')


class MarkedPostListView(LoginRequiredMixin, ListView):
    model = Post

    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(marked_by=self.request.user).order_by('-published_time')


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment_list.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by('-create_time')


class PostDetailView(DetailView):
    model = Post


class CreateDraftView(CreateView, LoginRequiredMixin):
    template_name = "post_form.html"
    form_class = PostForm


class UpdateDraftView(UpdateView, LoginRequiredMixin):
    template_name = "post_form.html"
    form_class = PostForm


class CreatePostView(CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.published_time = timezone.now()
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.published_time = timezone.now()
        return super().form_valid(form)


class CreateCommentView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    @staticmethod
    def save(request, pk):
        if request.method == 'POST':
            post = get_object_or_404(Post, pk=pk)
            print(request.body)
            comment = Comment(content=request.body.decode('utf-8'), author=request.user, post=post)
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})


# class DeleteCommentView(LoginRequiredMixin, DeleteView):
#     login_url = '/login/'
#     success_url = reverse_lazy('post_detail')
#     model = Comment
#     # template_name = 'blog/post_detail.html'


# 点赞博客
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # u = UserProfile.objects.filter(pk=request.user.id).first()
    if not request.user.liked_posts.filter(pk=post.pk):
        request.user.liked_posts.add(post)
        result = 1
    else:
        result = -1
        request.user.liked_posts.remove(post)
    return HttpResponse(result)


# 收藏博客
@login_required
def mark_post(request, pk):
    # if request.method == 'POST':
    post = get_object_or_404(Post, pk=pk)
    # u = UserProfile.objects.filter(pk=request.user.id).first()
    if not request.user.marked_posts.filter(pk=post.pk):
        result = 1
        request.user.marked_posts.add(post)
    else:
        result = -1
        request.user.marked_posts.remove(post)
    # return redirect('post_detail', pk=post.pk)
    return HttpResponse(result)


# 点赞评论
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # u = UserProfile.objects.filter(pk=request.user.id).first()
    if request.user.disliked_comments.filter(pk=pk):
        return HttpResponse(-1)
    if not request.user.liked_comments.filter(pk=pk):
        request.user.liked_comments.add(comment)
        request.user.disliked_comments.remove(comment)
        result = 1
    else:
        request.user.liked_comments.remove(comment)
        result = 0
    # return redirect('post_detail', pk=comment.post.pk)
    return HttpResponse(result)


# 点灭评论
@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # u = UserProfile.objects.filter(pk=request.user.id).first()
    if request.user.liked_comments.filter(pk=pk):
        return HttpResponse(-1)
    if not request.user.disliked_comments.filter(pk=pk):
        request.user.liked_comments.remove(comment)
        request.user.disliked_comments.add(comment)
        result = 1
    else:
        request.user.disliked_comments.remove(comment)
        result = 0
    # return redirect('post_detail', pk=comment.post.pk){}
    return HttpResponse(result)


# 移除评论
@login_required
def remove_comment(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)


# 博客阅读次数+1
@login_required
def add_view_count(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        post.viewed_count += 1
        post.save()
        return HttpResponse(post.viewed_count)
