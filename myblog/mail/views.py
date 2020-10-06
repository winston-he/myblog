import smtplib
from email.header import Header
from email.mime.text import MIMEText

from django.shortcuts import render

# Create your views here.
# from celery.task import task
from django.core.mail import send_mail

from myblog import settings
from .celery_cfg import Config
from celery import Celery, Task


app = Celery(__name__)
app.config_from_object(Config)


class EmailTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("send email failed")
        pass

    def on_success(self, retval, task_id, args, kwargs):
        print("send email succeeded")
        pass

@app.task(name='send_activate_email', bind=True, base=EmailTask)
def send_email(self, **kwargs):
    """
    :param self:
    :param kwargs:
    :return:
    """
    mail_host = settings.EMAIL_HOST  # 设置服务器
    mail_user = settings.EMAIL_HOST_USER  # 用户名
    mail_pass = settings.EMAIL_HOST_PASSWORD  # 口令
    sender = settings.EMAIL_FROM
    receivers = kwargs['recipient_list']
    message = MIMEText(kwargs['html_message'], 'html', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(".".join(receivers), 'utf-8')

    subject = kwargs['subject']
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())


