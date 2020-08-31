from django.db import models

# Create your models here.
from django.utils import timezone


class AccessLog(models.Model):
    request_user = models.CharField(max_length=100, null=True) # USER
    request_path = models.CharField(max_length=250) # PATH_INFO
    request_method = models.CharField(max_length=10) # REQUEST_METHOD
    remote_addr = models.CharField(max_length=128) # REMOTE_ADDR
    host_addr = models.CharField(max_length=128) # HTTP_HOST
    create_time = models.DateTimeField(default=timezone.now)
