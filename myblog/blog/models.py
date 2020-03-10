from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False)
    content = models.TextField(null=False)
    viewed_count = models.PositiveIntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    published_time = models.DateTimeField(null=True)

    liked_by = models.ManyToManyField(to='auth.User', related_name='liked_posts')
    marked_by = models.ManyToManyField(to='auth.User', related_name='marked_posts')

    # 发布
    def publish(self):
        self.published_time = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return '{} by {}'.format(self.title, self.author.username)


class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', related_name='post_comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=140, null=False, help_text="Please fill it in!")
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)

    liked_by = models.ManyToManyField(to='auth.User', related_name='liked_comments')
    disliked_by = models.ManyToManyField(to='auth.User', related_name='disliked_comments')

    def __str__(self):
        return self.content
