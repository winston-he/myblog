from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserChatInfo(models.Model):
    signature = models.CharField(max_length=140, null=True)
    user = models.OneToOneField(User, related_name='chat_info', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'user_chat_info'