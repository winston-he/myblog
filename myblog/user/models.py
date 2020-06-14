from django.contrib.auth.models import Permission, User
from django.db import models


class UserManager(models.Manager):
    # def save(self, name, password, email, gender):
    #     self.model()

    def get_queryset(self):
        return super(UserManager, self).get_queryset()


class UserProfile(models.Model):
    '''用户表'''

    class Meta:
        ordering = ['user__date_joined']
        verbose_name = '用户'

    gender_choices = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )

    gender = models.IntegerField(choices=gender_choices, default=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.user.get_username() + ' ' + self.user.email


#
# class ChatGroup(Group):
#     pass
#
#
# class TopicPermission(Permission):
#     pass
