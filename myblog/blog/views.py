import code
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Post, Comment, Appendix

# Create your views here.
# class AboutView(TemplateView):
#     template_name = 'about.html'
COMMENT_PER_PAGE = 5
BLOG_PER_PAGE = 1


class PostListView(ListView):
    model = Post
    paginate_by = 2

    def get_queryset(self, page=1):
        start = (page - 1) * BLOG_PER_PAGE
        end = start + BLOG_PER_PAGE
        return Post.objects.filter(published_time__isnull=False).order_by('-published_time')[start: end]

    # def get_posts_by_page(self, page):
    #
    #     return Post.objects.filter(published_tim'{%url "view_count" pk=0%}';e__isnull=False).order_by('-published_time')[start: end]


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
    paginate_by = 5

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by('-create_time')


class PostDetailView(DetailView):
    model = Post

    @staticmethod
    def get_total_comment_count(request, pk):
        res = Comment.objects.filter(post=pk).count()
        return JsonResponse({"total_comment_count": res, "comment_per_page": COMMENT_PER_PAGE})

    @staticmethod
    def post_comment_list(request, pk):
        page = request.GET.get('page')
        page = int(page)
        # 分页
        comments = Comment.objects.filter(post=pk).order_by("-likes_count")[
                   page * COMMENT_PER_PAGE:page * COMMENT_PER_PAGE + COMMENT_PER_PAGE]
        # code.interact(local=locals())
        last_page = len(comments) < COMMENT_PER_PAGE
        res = []
        for comment in comments:
            res.append({
                "id": comment.id,
                "author": comment.author.username,
                "post": pk,
                "content": comment.content,
                "likes_count": comment.likes_count,
                "dislikes_count": comment.dislikes_count,
                "created_time": comment.create_time.strftime("%b %d, %Y %I:%M %p"),
                "liked": request.user in comment.liked_by.all(),
                "disliked": request.user in comment.disliked_by.all()
            })
        return JsonResponse({"comment_list": res, "last_page": last_page}, safe=False)


class CreateDraftView(LoginRequiredMixin, CreateView):
    template_name = "blog/post_form.html"
    form_class = PostForm


class UpdateDraftView(LoginRequiredMixin, UpdateView):
    template_name = "blog/post_form.html"
    form_class = PostForm


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "blog/post_form.html"


    def form_valid(self, form):
        form.instance.published_time = timezone.now()
        return super().form_valid(form)

    # 新建并保存，但不发布
    @staticmethod
    @login_required
    def save(request):
        form = PostForm(request.POST)
        if form.is_valid() and request.is_ajax():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse(data={"pk": post.pk})
        else:
            print(form.cleaned_data)
            print(form.errors.as_data())
        return render(request, 'blog/post_form.html')


class UpdatePostView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_queryset(self):
        return Post.objects.filter(**self.kwargs)

    def form_valid(self, form):
        form.instance.published_time = timezone.now()
        return super().form_valid(form)

    # 更新并保存，但不发布
    def save(self, pk):
        form = PostForm(self.request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()

    def publish(self, pk):
        post = get_object_or_404(Post, pk=pk)
        post.published_time = timezone.now()
        post.save()
        return redirect('post_detail', pk=pk)


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


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
    # u = UserProfile.objects.filter(pk=request.registration.id).first()
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
    # u = UserProfile.objects.filter(pk=request.registration.id).first()
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
    # u = UserProfile.objects.filter(pk=request.registration.id).first()
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
    # u = UserProfile.objects.filter(pk=request.registration.id).first()
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
    if request.method == "POST" and request.is_ajax():
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return JsonResponse(data={'result': 0})


# 博客阅读次数+1
@login_required
def add_view_count(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        post.viewed_count += 1
        post.save()
        return HttpResponse(post.viewed_count)


@csrf_exempt
@xframe_options_sameorigin
def upload_image(request):
    if request.method == 'POST':
        data = {'success': 0, 'message': '图片上传失败'}
        print(data)
        image = request.FILES.get('editormd-image-file', None)
        if image:
            # 这里做图片存储的工作
            appendix = Appendix()
            appendix.file = image
            appendix.save()
            image_url = '/static/upload' + appendix.file.url  # 连接到图片位置的url
            data = {'success': 1, 'message': '图片上传成功', 'url': image_url}
        return JsonResponse(data, content_type="text/html")
