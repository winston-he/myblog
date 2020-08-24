from math import ceil

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, request, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.marsh import BlogPostPreviewSchema
from .forms import CommentForm, PostForm
from .models import Post, Comment, Appendix

# Create your views here.

COMMENT_PER_PAGE = 5
BLOG_PER_PAGE = 5


class PostListView(ListView):
    model = Post

    def get(self, request, *args, **kwargs):
        if self.get_queryset() == 'nonauthenticated':
            return redirect(reverse("login"))
        if self.request.is_ajax():
            schema = BlogPostPreviewSchema(many=True)
            schema.fields.pop("content")
            res = schema.dump(self.get_queryset())

            return JsonResponse({"result": "OK", "data": res})

        return super().get(request, *args, **kwargs)

    def get_queryset(self, page=1):
        all = True if self.request.GET.get("all") is not None and self.request.GET.get("all") == 'true' else False
        author_id = self.request.GET.get("author_id")
        published = True if self.request.GET.get("published") is not None and self.request.GET.get("published") == 'true' else False
        # 如果查询我的文章但是当前用户未登陆
        if not all and not self.request.user.is_authenticated:
            return "nonauthenticated"

        if all and not published:
            published = True

        self.template_name = 'blog/post_list.html' if all else 'blog/my_post_list.html'
        start = (page - 1) * BLOG_PER_PAGE
        end = start + BLOG_PER_PAGE
        if all:
            conditions = {
                "published_time__isnull": not published,
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
        return Post.objects.filter(**conditions).order_by('-published_time')[start: end]



    @staticmethod
    def get_posts_by_page(request, page):
        published = True if request.GET.get("all") == 'true' else False
        all = True if request.GET.get("all") is not None and request.GET.get("all") == 'true' else False

        conditions = {
            "published_time__isnull": not published,
        }
        if not all:
            conditions['author'] = request.user
        # TODO why page is a String??
        all_set = Post.objects.filter(**conditions).order_by('-published_time')
        pages = ceil(all_set.count() / BLOG_PER_PAGE)

        raw_set = all_set[(int(page))*BLOG_PER_PAGE: (int(page))*BLOG_PER_PAGE+BLOG_PER_PAGE]
        for record in raw_set:
            record.authorname = record.author.username
            record.liked_count = record.liked_by.count()
            record.marked_count = record.marked_by.count()
            record.comment_count = record.post_comments.count()

        schema = BlogPostPreviewSchema()
        res = schema.dump(raw_set, many=True)
        return JsonResponse(data={"data": res, "pages": pages}, safe=False)


class MarkedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    def get_queryset(self):
        return Post.objects.filter(marked_by=self.request.user).order_by('-published_time')


class PostDetailView(DetailView):
    model = Post

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
        form.instance.author = self.request.user
        form.instance.update_time = timezone.now()
        form.save()
        return JsonResponse({"result": 1, "msg": "OK", "pk": form.instance.pk})

    def form_invalid(self, form):
        print("hahah")
        return JsonResponse({"1": "1"})

class UpdatePostView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = "blog/post_form.html"



    def get_queryset(self):
        return Post.objects.filter(**self.kwargs)

    def form_valid(self, form):

        if form.cleaned_data['is_publish']:
            form.instance.published_time = timezone.now()

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
            res = []
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
        return Comment.objects.filter(post=int(self.kwargs['pk'])).order_by('-create_time')[(page-1)*limit: (page)*limit]


class CreateCommentView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Comment

    template_name = 'blog/comment_form.html'
    fields = ["content",]

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


# 移除评论
@login_required
def remove_comment(request, pk):
    if request.method == "POST" and request.is_ajax():
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return JsonResponse(data={'result': 0})


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
