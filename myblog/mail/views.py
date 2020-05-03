
from django.shortcuts import render

# Create your views here.
from celery.task import task
from django.core.mail import send_mail
from django.conf import settings


@task
def send_email(**kwargs):
    """
    django.core.mail.send_mail
    subject
    content
    from
    to: list
    html_message

    :param kwargs:
    :return:
    """
    return send_mail(**kwargs)

