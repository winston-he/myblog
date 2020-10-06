from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# from registration.models import UserProfile

POST_TYPE_CHOICES = ((0, '公开'),
                     (1, '仅订阅可见'),
                     (2, '私密'))

POST_STATUS_CHOICES = ((0, '草稿'),
                       (1, '审核中'),
                       (2, '已发布'),
                       (3, '举报通过'))

COMMENT_STATUS_CHOICES = ((0, '正常'),
                          (1, '审核中'),
                          (2, '已发布'),
                          (3, '举报审核'),
                          (4, '举报通过'))

VIOLATION_CHOICES = ((0, '正常'),
                          (1, '散布虚假信息'),
                          (2, '含有人身攻击、侮辱性言论'),
                          (3, '含有色情、暴力等不雅内容'),
                          (4, '侵犯著作权益'),
                          (5, '垃圾广告信息'),
                     (6, '其他'))

VIOLATION_REPORT_STATUS = ((0, '审核中'),
                           (1, '举报通过'),
                           (2, '举报驳回'))


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

    post_type = models.IntegerField(default=0, choices=POST_TYPE_CHOICES) # 0. 公开 1. 仅订阅的人可见 2. 私密
    status = models.IntegerField(default=0, choices=POST_STATUS_CHOICES) # 0. 草稿 1. 审核中 2. 已发布，状态正常 3. 举报通过

    # 发布
    def publish(self):
        self.published_time = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return '{} by {}'.format(self.title, self.author.username)

    class Meta:
        verbose_name = "博客"


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=140, null=False, help_text="Please fill it in!")
    create_time = models.DateTimeField(default=timezone.now)

    liked_by = models.ManyToManyField(to=User, related_name='liked_comments')
    disliked_by = models.ManyToManyField(to=User, related_name='disliked_comments')

    status = models.IntegerField(default=0, choices=COMMENT_STATUS_CHOICES) # 0. 正常 1. 举报审核 2. 举报通过

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"


class ViolationReport(models.Model):
    related_object_type = models.SmallIntegerField(null=False, choices=((0, '博客'), (1, '评论')), verbose_name="条目类型")
    related_object = models.IntegerField(null=False, verbose_name="相关条目")
    violation_type = models.SmallIntegerField(default=0, null=False, choices=VIOLATION_CHOICES, verbose_name="违规类型")
    status = models.SmallIntegerField(default=0, null=False, choices=VIOLATION_REPORT_STATUS, verbose_name="当前处理状态")
    comment = models.CharField(max_length=500, default='没有留言', verbose_name="举报用户留言")
    post_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_items', default=None, verbose_name="举报用户")
    handled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='handled_report_items', default=None, null=True, verbose_name="处理人")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=timezone.now, verbose_name="更新时间")

    def __str__(self):
        if self.related_object_type == 0:
            post = Post.objects.filter(pk=self.related_object).first()
            return "对博客: \"{}\"的举报".format(post.title)

        elif self.related_object_type == 1:
            comment = Comment.objects.filter(pk=self.related_object).first()
            return "对博客：\"{}\"中评论的举报".format(comment.post.title)

    class Meta:
        verbose_name = '举报记录'


class Appendix(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    # upload_to 相对于MEDIA_ROOT，媒体根目录，图片
    file = models.ImageField(upload_to='appendix/%Y/%m')