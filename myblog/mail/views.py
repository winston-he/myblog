from django.shortcuts import render

# Create your views here.
# from celery.task import task
from django.core.mail import send_mail
from .celery_cfg import Config
from celery import Celery, Task

app = Celery(__name__)
app.config_from_object(Config)


class EmailTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        pass

@app.task(name='send_activate_email', bind=True, base=EmailTask)
def send_email(self, **kwargs):
    """
    :param self:
    :param kwargs:
    :return:
    """
    return send_mail(fail_silently=False, **kwargs)
