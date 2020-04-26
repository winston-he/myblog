from django.shortcuts import reverse, render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import HttpResponse


# Create your views here.
# class AboutView(TemplateView):
#     template_name = 'about.html'
#
#
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        print("get posts")
        return Post.objects.filter(published_time__isnull=False).order_by('-published_time')


class DraftListView(ListView):
    model = Post

    def get_queryset(self):
        print("getting drafts")
        return Post.objects.filter(published_time__isnull=True).order_by('-published_time')


#
#
# class DraftListView(LoginRequiredMixin, ListView):
#     model = Post
#     redirect_field_name = 'post_list.html'
#     def get_queryset(self):
#         return Post.objects.filter(published_time__isnull=True).order_by('-create_time')
#
#
class PostDetailView(DetailView):
    model = Post
    # def get_object(self, queryset=None):
    #     post = super().get_object()
    #     post.viewed_count += 1
    #     post.save()
    #     self.viewed_count = post.viewed_count
    #     return post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    @staticmethod
    def save(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    @staticmethod
    def publish(request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect('post_detail', pk=pk)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm


class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = reverse_lazy('post_list')
    model = Post


class CreateCommentView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    @staticmethod
    def save(request, pk):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            post = get_object_or_404(Post, pk=pk)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})


# class DeleteCommentView(LoginRequiredMixin, DeleteView):
#     login_url = '/login/'
#     success_url = reverse_lazy('post_list')
#     model = Comment
#     # template_name = 'blog/post_detail.html'


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.liked_posts.filter(pk=post.pk):
        request.user.liked_posts.add(post)
        result = 1
    else:
        result = -1
        request.user.liked_posts.remove(post)
    return HttpResponse(result)


@login_required
def mark_post(request, pk):
    # if request.method == 'POST':
    post = get_object_or_404(Post, pk=pk)
    if not request.user.marked_posts.filter(pk=post.pk):
        result = 1
        request.user.marked_posts.add(post)
    else:
        result = -1
        request.user.marked_posts.remove(post)
    # return redirect('post_detail', pk=post.pk)
    return HttpResponse(result)


@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
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


@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
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


@login_required
def remove_comment(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return HttpResponse(1)


@login_required
def add_view_count(request, pk):
    if request.method == "POST":
        print("ADD VIEW COUNT")
        post = get_object_or_404(Post, pk=pk)
        post.viewed_count += 1
        post.save()
        return HttpResponse(post.viewed_count)

