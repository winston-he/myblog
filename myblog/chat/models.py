from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class UserChatInfo(models.Model):
    signature = models.CharField(max_length=140, null=True, default="还没有签名哦~")
    user = models.OneToOneField(User, related_name='chat_info', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'user_chat_info'


class PrivateChatRecord(models.Model):
    user_1 = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, related_name="user_one")
    user_2 = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, related_name="user_two")
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)

