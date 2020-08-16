from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.db import models


ACADEMY_LIMITS = 6
EMPLOYMENT_LIMITS = 10


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

def education_limit(value):
    if UserEducation.objects.filter(user=value) > ACADEMY_LIMITS:
        raise ValidationError("最多只能添加{}个教育经历".format(ACADEMY_LIMITS))

class UserEducation(models.Model):
    degree_choices = (
        ((0, '小学'), (1, '初中'), (2, '高中'),
         (3, '职高'),
         (4, '大专'),
         (5, '本科'),
         (6, '硕士研究生'),
         (7, '博士研究生'),
         (8, '博士导师'))
    )

    edu_school = models.CharField(max_length=50, null=True)
    edu_major = models.CharField(max_length=50, null=True)
    edu_degree = models.CharField(max_length=10, null=True, choices=degree_choices)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education', validators=(education_limit, ))

    def __str__(self):
        return "Academy: {}, Major: {}".format(self.edu_school, self.edu_major)


def employment_limit(value):
    if UserEducation.objects.filter(user=value) > ACADEMY_LIMITS:
        raise ValidationError("最多只能添加{}个工作经历".format(EMPLOYMENT_LIMITS))

class UserEmploymentInfo(models.Model):
    company = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employment', validators=(employment_limit, ))

    def __str__(self):
        return "Company: {}, Title: {}".format(self.company, self.title)

#
# class ChatGroup(Group):
#     pass
#
#
# class TopicPermission(Permission):
#     pass
