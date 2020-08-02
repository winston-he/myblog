from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from mail.mail_string import get_activate_msg
from mail.views import send_email
from .forms import UserForm

from .models import User, UserProfile
from myblog.settings import EMAIL_FROM
import os
from .utils import generate_token, load_token
from itsdangerous import SignatureExpired, BadSignature


class UserRegisterView(CreateView):
    form_class = UserForm
    template_name = 'register.html'

    def get_queryset(self):
        return User.objects.all()

    # def form_invalid(self, form):
    #     print(form.errors.as_json())
    #     return HttpResponse("表单验证失败")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        gender = form.cleaned_data['gender']
        # registration = User(username=username, password=password, email=email, is_active=0)
        user = User.objects.create_user(username, email, password)
        user.save()
        UserProfile(gender=gender, user=user).save()

        host = self.request.get_host()
        send_email.delay(subject="Myblog账号激活验证提醒",
                         message='',
                         from_email=EMAIL_FROM,
                         recipient_list=[email, ],
                         html_message=get_activate_msg(username, "{}/{}/{}".format(host, 'registration/activate',
                                                                             generate_token({"username": username})))

                         )
        print("邮件发送完毕")
        return render(self.request, 'activate.html', context={
            "username": username,
            "email": email
        })

def reset_password_done(request):
    if request.method == 'GET':
        return render(request, 'reset_password_done.html')



def activate_user_account(request):
    if request.method == 'GET':
        token = request.args.get("token", None, str)
        try:
            res = load_token(token)
        except SignatureExpired:
            HttpResponse("已经超过24小时，链接失效")
        except BadSignature:
            HttpResponse("您使用的为非法链接，可能经过篡改")
        else:
            username = res['username']
            User.objects.filter(name=username).update(activated=1)
            HttpResponse("您的账号已激活")

