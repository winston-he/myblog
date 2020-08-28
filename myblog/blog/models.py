from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# from registration.models import UserProfile


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False)
    content = models.TextField(null=False)
    viewed_count = models.PositiveIntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    published_time = models.DateTimeField(null=True)
    liked_by = models.ManyToManyField(to=User, related_name='liked_posts')
    marked_by = models.ManyToManyField(to=User, related_name='marked_posts')

    post_type = models.IntegerField(default=0) # 0. 公开 1. 仅订阅的人可见 2. 私密
    status = models.IntegerField(default=0) # 0. 草稿 1. 审核中 2. 已发布 3. 举报审核 4. 举报通过

    # 发布
    def publish(self):
        self.published_time = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return '{} by {}'.format(self.title, self.author.username)


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=140, null=False, help_text="Please fill it in!")
    create_time = models.DateTimeField(default=timezone.now)

    liked_by = models.ManyToManyField(to=User, related_name='liked_comments')
    disliked_by = models.ManyToManyField(to=User, related_name='disliked_comments')

    status = models.IntegerField(default=0) # 0. 正常 1. 举报审核 2. 举报通过

    def __str__(self):
        return self.content


class Appendix(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    # upload_to 相对于MEDIA_ROOT，媒体根目录，图片
    file = models.ImageField(upload_to='appendix/%Y/%m')