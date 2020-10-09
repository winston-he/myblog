from functools import reduce
from math import ceil

import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, JsonResponse, request, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.marsh import BlogPostPreviewSchema
from .forms import CommentForm, PostForm, ViolationReportForm
from .models import Post, Comment, Appendix, ViolationReport, VIOLATION_CHOICES

# Create your views here.

COMMENT_PER_PAGE = 5
BLOG_PER_PAGE = 5


# some signals
NONAUTHENTICATED = 'nonauthenticated'

class PostListView(ListView):
    model = Post

    def get(self, request, *args, **kwargs):
        if self.get_queryset() == NONAUTHENTICATED:
            return redirect(reverse("login"))
        if self.request.is_ajax():
            schema = BlogPostPreviewSchema(many=True)
            schema.fields.pop("content")
            res = schema.dump(self.get_queryset())
            for r in res:
                r['content'] = markdown.markdown(r['content'][:140])

            return JsonResponse({"result": "OK", "data": res})

        return super().get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        all = self.request.GET.get('all')
        context['all'] = all
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        page = self.request.GET.get("page")
        if page is None:
            print("page is None")
            page = 1
        else:
            page = int(page)

        all = True if self.request.GET.get("all") is not None and self.request.GET.get("all") == 'true' else False
        author_id = self.request.GET.get("author_id")
        published = True if self.request.GET.get("published") is not None and self.request.GET.get(
            "published") == 'true' else False
        # 如果查询我的文章但是当前用户未登陆
        if not all and not self.request.user.is_authenticated and not author_id:
            return NONAUTHENTICATED

        if all and not published:
            published = True

        self.template_name = 'blog/post_list.html' if all else 'blog/my_post_list.html'
        start = (page - 1) * BLOG_PER_PAGE
        end = start + BLOG_PER_PAGE
        # 所有人的
        if all:
            conditions = {
                "status": 2
            }
        else:
            conditions = {}
        if not all:
            if author_id is None:
                conditions['author'] = self.request.user
            else:
                conditions['author'] = get_object_or_404(User, pk=int(author_id))
                post_list_type = self.request.GET.get("type")
                if post_list_type == "popular":
                    return Post.objects.filter(**conditions).order_by('-viewed_count')[:5]
                else:
                    return Post.objects.filter(**conditions).order_by('-published_time')[:5]
        raw_set = Post.objects.filter(**conditions).order_by('-published_time')[start: end]
        for record in raw_set:
            record.liked_count = record.liked_by.count()
            record.marked_count = record.marked_by.count()
            record.comment_count = record.post_comments.count()
        return raw_set


class MarkedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(marked_by=self.request.user).order_by('-published_time')


class PostAuthorInfo(DetailView):
    model = User

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        res = {}
        cursor = connection.cursor()
        cursor.execute(f"select count(1) from user_userprofile_subscribe_to where user_id={self.object.id}")
        res['subscribe_count'] = cursor.fetchone()[0]

        posts = Post.objects.filter(author=self.object, status=2)

        res['author_like_count'] = 0
        for p in posts:
            res['author_like_count'] += p.liked_by.count()
        return JsonResponse({"data": res, "msg": "OK", "status": 200})

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # author_follow_count
        # author_likes
        # author_blog_count
        cursor = connection.cursor()
        cursor.execute(f"select count(1) from user_userprofile_subscribe_to where user_id={self.object.author.id}")
        res = cursor.fetchone()
        kwargs['author_subscribe_count'] = res

        return super().get_context_data(**kwargs)


    @staticmethod
    def get_total_comment_count(request, pk):
        res = Comment.objects.filter(post=pk).count()
        return JsonResponse({"total_comment_count": res, "comment_per_page": COMMENT_PER_PAGE})


class CreateDraftView(LoginRequiredMixin, CreateView):
    template_name = "blog/post_form.html"
    form_class = PostForm

    # def form_valid(self, form):
    #     super().form_valid(form)
    #     self.object

    def get_success_url(self):
        return reverse('post_detail', {"pk": self.object.pk})


class UpdateDraftView(LoginRequiredMixin, UpdateView):
    template_name = "blog/post_form.html"
    form_class = PostForm


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        if form.cleaned_data['is_publish']:
            form.instance.published_time = timezone.now()
            form.instance.status = 1 # 审核中
        form.instance.author = self.request.user
        form.instance.update_time = timezone.now()
        form.save()
        if not self.request.is_ajax():
            self.kwargs['pk'] = form.instance.pk
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs=self.kwargs)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_queryset(self):
        return Post.objects.filter(**self.kwargs)

    def form_valid(self, form):

        if form.cleaned_data['is_publish']:
            form.instance.published_time = timezone.now()
            form.instance.status = 1 # 审核中, 审核后才可公布

        form.instance.update_time = timezone.now()
        if self.request.is_ajax():
            form.save()
            return JsonResponse({"result": 1, "msg": "OK", "pk": form.instance.pk})
        else:
            return super().form_valid(form)

    def get_success_url(self):
        print("Hello World")
        return reverse('post_detail', kwargs=self.kwargs)


class DeletePostView(LoginRequiredMixin, DeleteView):
    # model = Post
    success_url = reverse_lazy('post_list', **{"all": "false"})

    def get_queryset(self):
        return

    def get_object(self, queryset=None):
        return

    def delete(self, request, *args, **kwargs):
        # 不重定向，而是返回ajax response
        if request.is_ajax():
            post_pk = int(kwargs['pk'])
            post = Post.objects.filter(pk=post_pk).first()
            if post is None or post.author != self.request.user:
                return JsonResponse({"result": -1, "msg": "删除失败！"})
            else:
                post.delete()
                return JsonResponse({"result": 1, "msg": "删除成功"})
        else:
            super().delete(request, *args, **kwargs)


class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comment_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        # 直接返回json格式的数据
        if self.request.is_ajax():
            query_set = self.get_queryset()

            if query_set == NONAUTHENTICATED:
                return redirect(reverse("login"))
            res = []

            # comment的总数
            total_comment = Comment.objects.filter(post=int(kwargs['pk'])).count()
            for record in query_set:
                res.append({
                    "pk": record.pk,
                    "author": record.author.username,
                    "create_time": record.create_time.strftime("%b %d, %Y %I:%M %p"),
                    "content": record.content,
                    "likes_count": record.liked_by.count(),
                    "dislikes_count": record.disliked_by.count(),
                    "is_liked": self.request.user in record.liked_by.all(),
                    "is_disliked": self.request.user in record.disliked_by.all()
                })
            return JsonResponse({"data": res, "result": 1, "total_comment": total_comment, "limit": self.paginate_by})
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        limit = self.paginate_by
        page = self.request.GET.get('page', None)
        page = 1 if page is None else int(page)
        condition = {
            "post": int(self.kwargs['pk'])
        }

        return Comment.objects.filter(**condition).order_by('-create_time')[
               (page - 1) * limit: (page) * limit]


class MyCommentList(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'blog/my_comment_list.html'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            comment_count = Comment.objects.filter(author=self.request.user).count()
            query_set = self.get_queryset()
            res = []
            for item in query_set:
                res.append({
                    "pk": item.pk,
                    "post": item.post.title,
                    "post_pk": item.post.pk,
                    "create_time": item.create_time.strftime("%b %d, %Y %I:%M %p"),
                    "likes": item.liked_by.count(),
                    "dislikes": item.disliked_by.count(),
                    "content": item.content
                })
            return JsonResponse({"result": 1, "data": res, "total_comment": comment_count, "limit": self.paginate_by})
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        limit = self.paginate_by
        page = self.request.GET.get('page', None)
        page = 1 if page is None else int(page)
        return Comment.objects.filter(author=self.request.user).order_by('-create_time')[
               (page - 1) * limit: (page) * limit]


class CreateCommentView(CreateView):
    login_url = '/login/'
    model = Comment

    template_name = 'blog/comment_form.html'
    fields = ["content", ]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"result": -1, "msg": "not logged in yet"})
        return super().get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['pk'] = self.kwargs['pk']
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=int(self.kwargs['pk']))
        # 执行成功后不重定向，而是返回JsonResponse
        form.save()
        return JsonResponse({"result": 1, "data": {
            "pk": form.instance.pk,
            "create_time": form.instance.create_time.strftime("%b %d, %Y %I:%M %p"),
            "content": form.instance.content,
            "likes_count": form.instance.liked_by.count(),
            "dislikes_count": form.instance.disliked_by.count(),
            "author": self.request.user.username
        }})

    def form_invalid(self, form):
        return JsonResponse({"result": -1})


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Comment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.pk
        if self.object.author == self.request.user:
            self.object.delete()
            return JsonResponse({"result": 0, "msg": "操作成功", "pk": pk})
        else:
            return JsonResponse({"result": -1, "msg": "操作失败", "pk": pk})


class SubscribeListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'blog/my_subscribes.html'

    def get(self, request, *args, **kwargs):

        total_subscribes = self.request.user.user.subscribe_to.count()
        if self.request.is_ajax():
            raw_set = self.get_queryset()
            res = []
            for item in raw_set:
                res.append({
                    "pk": item.pk,
                    "username": item.username,
                    "profile": "",
                    "subscribe_count": 0,
                    "post_count": Post.objects.filter(author=item).count()
                })
            return JsonResponse(
                {"result": 1, "data": res, "total_subscribes": total_subscribes, "limit": self.paginate_by})
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        page = self.request.GET.get('page', 1)
        page = int(page)
        # return self.request.user.user.subscribe_to[(page-1)*self.paginate_by:page*self.paginate_by]
        return self.request.user.user.subscribe_to.all()


class ReportViolationView(LoginRequiredMixin, CreateView):
    model = ViolationReport
    # fields = ['violation_type', 'comment']
    template_name = 'blog/report_violation_form.html'
    form_class = ViolationReportForm

    def render_to_response(self, context, **response_kwargs):
        context['violation_type'] = list(VIOLATION_CHOICES)
        context['violation_type'].pop(0)
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        print("hello world")
        form.instance.related_object_type = self.kwargs['type']
        form.instance.related_object = self.kwargs['pk']
        form.instance.post_by = self.request.user

        return super().form_valid(form)


# 点赞博客
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.liked_posts.filter(pk=post.pk):
        request.user.liked_posts.add(post)
        result = 1
    else:
        result = -1
        request.user.liked_posts.remove(post)
    return JsonResponse({"result": result})


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
    return JsonResponse({"result": result})


# 点赞评论
@login_required
def like_comment(request, pk):
    """
    :param request:
    :param pk:
    :return:
    如果已经点灭，返回-1，提示不能操作
    如果已经点赞，返回1，取消点赞
    如果没有点赞，返回0，加入点赞
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.disliked_comments.filter(pk=pk):
        result = -1
    elif not request.user.liked_comments.filter(pk=pk):
        request.user.liked_comments.add(comment)
        request.user.disliked_comments.remove(comment)
        result = 0
    else:
        request.user.liked_comments.remove(comment)
        result = 1
    return JsonResponse({"result": result, "pk": pk})


# 点灭评论
@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.liked_comments.filter(pk=pk):
        result = -1
    elif not request.user.disliked_comments.filter(pk=pk):
        request.user.liked_comments.remove(comment)
        request.user.disliked_comments.add(comment)
        result = 0
    else:
        request.user.disliked_comments.remove(comment)
        result = 1
    return JsonResponse({"result": result, "pk": pk})


# 博客阅读次数+1
@login_required
def increase_view_count(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        # 只对已发布的文章更新此数字
        if post.published_time:
            post.viewed_count += 1
            post.save()
        return JsonResponse(post.viewed_count, safe=False)


# 一些数据统计
@login_required
def personal_summary(request):
    from collections import defaultdict

    res = defaultdict(int)
    res['my_blog_count'] = Post.objects.filter(published_time__isnull=False, author=request.user).count()
    for p in Post.objects.filter(published_time__isnull=False, author=request.user):
        res["total_likes_count"] += p.liked_by.count()
        res["total_marked_count"] += p.marked_by.count()
        res["total_visit_count"] += p.viewed_count
    return JsonResponse(res)


@csrf_exempt
@xframe_options_sameorigin
def upload_image(request):
    if request.method == 'POST':
        data = {'success': 0, 'message': '图片上传失败'}
        print(data)
        image = request.FILES.get('editormd-image-file', None)
        if image:
            # 这里做图片存储
            appendix = Appendix()
            appendix.file = image
            appendix.save()
            image_url = '/static/upload' + appendix.file.url  # 连接到图片位置的url
            data = {'success': 1, 'message': '图片上传成功', 'url': image_url}
        return JsonResponse(data, content_type="text/html")
