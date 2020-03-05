from django.shortcuts import  reverse, render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.
# class AboutView(TemplateView):
#     template_name = 'about.html'
#
#
class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_time__isnull=False).order_by('-published_time')
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
#
#
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
    def publish(pk):
        Post.objects.filter(pk=pk).update(published_time=timezone.now())
#
#
class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm
#
#
class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = reverse_lazy('post_list')
#
#
# class CreateCommentView(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'post_detail.html'
#     model = Comment
#     form_class = CommentForm
#
#
#
#
# class DeleteCommentView(LoginRequiredMixin, DeleteView):
#     login_url = '/login/'
#     success_url = reverse('post_detail')


# class AboutView(TemplateView):
#     template_name = 'about.html'
#
#
# class PostListView(ListView):
#     model = Post
#
#     def get_queryset(self):
#         return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#
#
# class PostDetailView(DetailView):
#     model = Post
#
#
# class CreatePostView(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#
#     form_class = PostForm
#     model = Post
#
#     @staticmethod
#     def post_publish(request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         post.publish()
#         return redirect('post_detail', pk=pk)
#
#
# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#
#     form_class = PostForm
#
#     model = Post
#
#
# class DraftListView(LoginRequiredMixin, ListView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_list.html'
#
#     model = Post
#
#     # posts that had not been published
#     def get_queryset(self):
#         return Post.objects.filter(published_date__isnull=True).order_by('created_date')
#
#
# class PostDeleteView(LoginRequiredMixin, DeleteView):
#     model = Post
#     success_url = reverse_lazy('post_list')
#
#
# #######################################
# ## Functions that require a pk match ##
# #######################################
#
# # @login_required
# # def post_publish(request, pk):
# #     post = get_object_or_404(Post, pk=pk)
# #     post.publish()
# #     return redirect('post_detail', pk=pk)
#
# @login_required
# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/comment_form.html', {'form': form})
#
#
# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', pk=comment.post.pk)
#
#
# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     post_pk = comment.post.pk
#     comment.delete()
#     return redirect('post_detail', pk=post_pk)