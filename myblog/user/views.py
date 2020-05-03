from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render

from mail.mail_string import get_activate_msg
from mail.views import send_email
from .forms import UserForm
from .models import User
from myblog.settings import EMAIL_FROM
import os
from .utils import generate_token, load_token

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        gender = int(request.POST.get("gender"))
        if password != confirm_password:
            return HttpResponse("两次输入的密码不一致")
        u = User.objects.filter(name=username).first()
        if u:
            return HttpResponse("系统中已存在此用户") if u.is_activated else HttpResponse("请查看邮箱中的激活邮件，并完成激活验证")

        password = make_password(password)
        User(name=username, password=password, email=email, gender=gender).save()
        host = request.get_host()
        print(host)
        send_email.delay(subject="Myblog账号验证提醒", message='', from_email=EMAIL_FROM, recipient_list=[email, ],
                         html_message=get_activate_msg(username, "{}/{}/{}".format(host, 'user/activate', generate_token({"username": username}))))
        return render(request, 'activate.html', context={
            "username": username,
            "email": email
        })
    return render(request, 'user_form.html')


def activate_user_account():
    pass

