from django.shortcuts import reverse, render, get_object_or_404, redirect
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
        # return Post.objects.filter(published_time__isnull=False).order_by('-published_time')
        return Post.objects.order_by('-published_time')


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
    # template_name = 'blog/comment_form.html'
    # model = Comment
    # form_class = CommentForm
    # success_url = reverse_lazy('post_detail')

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


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = reverse_lazy('post_list')
    model = Comment
    # template_name = 'blog/post_detail.html'
