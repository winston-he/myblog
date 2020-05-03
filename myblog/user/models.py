from django.db import models


class UserManager(models.Manager):
    # def save(self, name, password, email, gender):
    #     self.model()

    def get_queryset(self):
        return super(UserManager, self).get_queryset()


class User(models.Model):
    '''用户表'''

    gender_choices = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    gender = models.IntegerField(choices=gender_choices, default=2)
    is_activated = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_time']
        verbose_name = '用户'



