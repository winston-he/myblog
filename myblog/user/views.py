from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from mail.mail_string import get_activate_msg
from mail.views import send_email
from .forms import UserRegisterForm, PersonalInfoForm

from .models import User, UserProfile
from myblog.settings import EMAIL_FROM
import os
from .utils import generate_token, load_token
from itsdangerous import SignatureExpired, BadSignature


class UpdatePersonalInfoView(LoginRequiredMixin, UpdateView):
    template_name = "profile/personal_info_form.html"
    model = User
    form_class = PersonalInfoForm

    def form_valid(self, form):
        form.cleaned_data

        return super().form_valid(form)

class PersonalInfoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile/my_zone.html'
    model = User

def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            UserProfile(user=user).save()
            host = request.get_host()
            send_email.delay(subject="Myblog账号激活验证提醒",
                             message='',
                             from_email=EMAIL_FROM,
                             recipient_list=[form.cleaned_data['email'], ],
                             html_message=get_activate_msg(form.cleaned_data['username'], "{}/{}/{}".format(host, 'registration/activate',
                                                                                       generate_token({"username": form.cleaned_data['username']}))),
                             expires=2)
            print("邮件发送完毕")
            # return redirect(reverse('activate_user'))
            return render(request, 'registration/activate.html', context={
                "username": form.cleaned_data['username'],
                "email": form.cleaned_data['email']
            })
        else:
            errors = form.errors.as_data()
            for key in errors.keys():
                for e in errors[key]:
                    print(e.messages)
                    errors[key] = " ".join(e.messages)
            return render(request, 'registration/login.html', context={"action_type": "register", "errors": errors})



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

