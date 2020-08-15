from django.contrib.auth.models import Permission, User
from django.db import models


class UserManager(models.Manager):
    # def save(self, name, password, email, gender):
    #     self.model()

    def get_queryset(self):
        return super(UserManager, self).get_queryset()


class UserProfile(models.Model):
    '''用户、用户信息'''

    class Meta:
        ordering = ['user__date_joined']
        verbose_name = '用户'

    gender_choices = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', null=True)
    nickname = models.CharField(max_length=50, null=True)
    gender = models.IntegerField(choices=gender_choices, default=2)
    introduction = models.CharField(max_length=300, null=True)
    profile_image = models.ImageField(upload_to='profile/%Y/%m', null=True)
    location = models.CharField(max_length=100, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.nickname is None:
            self.nickname = self.user.get_username()
        super().save()

    def __str__(self):
        return self.user.get_username() + ' ' + self.user.email


class UserEducation(models.Model):
    edu_school = models.CharField(max_length=50, null=True)
    edu_major = models.CharField(max_length=50, null=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')

    def __str__(self):
        return "Academy: {}, Major: {}".format(self.edu_school, self.edu_major)

class UserEmploymentInfo(models.Model):
    company = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employment')

    def __str__(self):
        return "Company: {}, Title: {}".format(self.company, self.title)

#
# class ChatGroup(Group):
#     pass
#
#
# class TopicPermission(Permission):
#     pass
