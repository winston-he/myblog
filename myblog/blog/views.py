from math import ceil

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, request
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
        return super().get(request, *args, **kwargs)
    def get_queryset(self, page=1, all=True, published=False):

        all = True if self.request.GET.get("all") is not None and self.request.GET.get("all") == 'true' else False
        # 如果查询我的文章但是当前用户未登陆
        if not all and not self.request.user.is_authenticated:
            return "nonauthenticated"

        self.template_name = 'blog/post_list.html' if all else 'blog/my_post_list.html'
        start = (page - 1) * BLOG_PER_PAGE
        end = start + BLOG_PER_PAGE
        conditions = {
            "published_time__isnull": not published,
        }
        if not all:
            conditions['author'] = self.request.user
        res = Post.objects.filter(**conditions).order_by('-published_time')[start: end]
        return res


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
        form.instance.published_time = timezone.now()
        form.instance.author = self.request.user
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


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'blog/comment_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            query_set = self.get_queryset()
            res = []
            for record in query_set:
                res.append({
                    "create_time": record.create_time.strftime("%b %d, %Y %I:%M %p"),
                    "content": record.content,
                    "likes_count": record.liked_by.count(),
                    "dislikes_count": record.disliked_by.count()
                })
            return JsonResponse({"data": res, "result": 1})
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        limit = self.paginate_by
        page = self.request.GET.get('page', None)
        page = 1 if page is None else int(page)
        return Comment.objects.filter(author=self.request.user).order_by('-create_time')[page*limit: (page+1)*limit]


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
        return JsonResponse({"result": 1})

    def form_invalid(self, form):
        return JsonResponse({"result": -1})


# class DeleteCommentView(LoginRequiredMixin, DeleteView):
#     login_url = '/login/'
#     success_url = reverse_lazy('post_detail')
#     model = Comment
#     # template_name = 'blog/post_detail.html'


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
