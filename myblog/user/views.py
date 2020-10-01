import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, LoginView
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, FormView
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer as Serializer

from chat.chat_user import create_chat_user
from chat.decorators import webim_token_check
from chat import *
from chat.models import UserChatInfo
from mail.views import send_email
from myblog.settings import EMAIL_FROM
from .forms import UserRegisterForm, PersonalInfoForm, PasswordResetForm
from .models import User, UserProfile, UserPreference
from .utils import generate_token, load_token



class MyLoginView(LoginView):
    success_url = reverse_lazy("post_list")

    def dispatch(self, request, *args, **kwargs):
        print("hello world")
        username = self.request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user is not None and user.is_active == 0:
            return render(self.request, 'registration/login.html',
                          context={"action_type": "login", "errors": "该用户没有被激活，请前往邮箱进行激活"})
        return super().dispatch(request, *args, **kwargs)


class MyLogoutView(LogoutView):
    # def re
    pass


class PasswordReset(PasswordResetView):
    def form_valid(self, form):
        user = get_object_or_404(User, email=form.cleaned_data['email'])

        if user is not None and user.is_active == 0:
            return render(self.request, 'generic/message.html', context={"message": "该用户没有被激活，请先通过邮箱中的激活邮件进行激活"})

        # 30 分钟超时
        serializer = Serializer("secret-key", salt="myblog-jws", expires_in=3600 * 30)
        token = serializer.dumps({
            "username": user.username,

        }).decode('utf-8')
        link = "http://{}/{}/{}".format(self.request.META.get('HTTP_HOST'), 'registration/password/reset', token)
        print(link)
        send_email.delay(subject="Myblog密码重置",
                         message='',
                         from_email=EMAIL_FROM,
                         recipient_list=[form.cleaned_data['email'], ],
                         html_message=render_to_string('mail/reset_password.html', context={"username": user.username,
                                                                                            "link": link}),
                         expires=2)
        return render(self.request, 'registration/password_reset_hint.html')


class PasswordResetConfirm(FormView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = PasswordResetForm

    def form_valid(self, form):

        token = self.kwargs['token']
        serializer = Serializer("secret-key", salt="myblog-jws", expires_in=3600 * 30)

        try:
            info = serializer.loads(token)
        except SignatureExpired:
            return render(self.request, 'generic/message.html', context={"message": "您的链接已过期，请重新获取"})
        except BadSignature:
            return render(self.request, 'generic/message.html', context={"message": "您的链接可能遭到恶意篡改，请重新获取"})

        curr_user = User.objects.get(username=info['username'])
        # 更新密码
        curr_user.set_password(form.cleaned_data['password'])
        curr_user.save()

        return render(self.request, 'generic/message.html', context={"message": "您的密码已成功修改"})

    def form_invalid(self, form):
        print("hahaha")
        return super().form_invalid(form)


class UpdatePersonalInfoView(LoginRequiredMixin, UpdateView):
    template_name = "profile/personal_info_form.html"
    model = User
    form_class = PersonalInfoForm

    def get_success_url(self):
        return reverse("my_zone", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        location = "{}#{}#{}".format(cleaned_data['location1'],
                                     cleaned_data['location2'],
                                     cleaned_data['location3'])
        self.request.user.user.location = location
        self.request.user.user.introduction = cleaned_data['introduction']
        self.request.user.user.nickname = cleaned_data['nickname']
        self.request.user.user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class PersonalInfoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile/my_zone.html'
    model = User


def update_preference_setting(request, pk):
    r_access = request.POST.get("record_access")
    edu_access = request.POST.get("education_access")
    emp_access = request.POST.get("employment_access")
    d = {
        "on": True,
        "off": False
    }

    update_data = {}
    if r_access is not None:
        update_data['record_access'] = d[r_access]
    if edu_access is not None:
        update_data['education_access'] = d[edu_access]
    if emp_access is not None:
        update_data['employment_access'] = d[emp_access]
    if request.user.preference is None:
        update_data['user'] = request.user
        UserPreference(**update_data).save()
    else:
        request.user.preference.update(**update_data)
    return JsonResponse({"result": 0, "msg": "更新成功"})


@webim_token_check
def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']):
                return render(request, 'registration/login.html',
                              context={"action_type": "register", "errors": "系统中已存在该用户名"})
            if User.objects.filter(email=form.cleaned_data['email']):
                return render(request, 'registration/login.html',
                              context={"action_type": "register", "errors": "系统中已存在同名的邮箱"})
            user = User.objects.create_user(**form.cleaned_data)
            user.is_active = 0
            user.save()

            UserProfile(user=user).save()
            UserPreference(user=user).save()
            # 聊天: 创建一个聊天用户
            # create_chat_user(form.cleaned_data['username'], form.cleaned_data['password'])


            host = request.get_host()
            link = "http://{}/{}/{}".format(host, 'registration/activate',
                                            generate_token({"username":
                                                                form.cleaned_data[
                                                                    'username']}))
            print(link)
            send_email.delay(subject="Myblog账号激活验证提醒",
                             message='',
                             from_email=EMAIL_FROM,
                             recipient_list=[form.cleaned_data['email'], ],
                             html_message=render_to_string('generic/message.html',
                                                           context={"message": "请点击以下链接以激活账号: " + link}),
                             expires=2)
            return render(request, 'registration/activate.html', context={
                "username": form.cleaned_data['username'],
                "email": form.cleaned_data['email']
            })
        else:
            errors = form.errors.as_data()
            for key in errors.keys():
                for e in errors[key]:
                    errors[key] = " ".join(e.messages)
            return render(request, 'registration/login.html', context={"action_type": "register", "errors": errors})


# 关注/取关
@login_required
def subscribe(request, pk):
    subscribe_to = User.objects.filter(pk=pk).first()
    # 关注
    if subscribe_to and subscribe_to not in request.user.user.subscribe_to.all():
        request.user.user.subscribe_to.add(subscribe_to)
        result = 0
    # 取关
    else:
        request.user.user.subscribe_to.remove(subscribe_to)
        result = 1
    request.user.user.save()
    return JsonResponse({"result": result, "msg": "操作成功"})


class ProfileImageView(LoginRequiredMixin, View):

    def get(self, request):
        response = FileResponse(self.request.user.user.profile_image)
        response['Content-Type'] = 'application/octet-stream'
        filename = 'attachment; filename=' + '{}.png'.format('xxx')
        # TODO 设置文件名的包含中文编码方式
        response['Content-Disposition'] = filename.encode('utf-8', 'ISO-8859-1')
        return response

    def post(self, request):
        file = self.request.FILES['file']
        self.request.user.user.profile_image = file
        self.request.user.user.save()
        return JsonResponse({"result": 0, "msg": "图片上传成功"})


@login_required
def upload_profile_picture(request):
    file = request.FILES['file']
    request.user.user.profile_image = file
    request.user.user.save()
    return JsonResponse({"result": 0, "msg": "图片上传成功"})

def reset_password_done(request):
    if request.method == 'GET':
        return render(request, 'reset_password_done.html')


def activate_user_account(request, token):
    if request.method == 'GET':
        try:
            res = load_token(token)
        except SignatureExpired:
            return render(request, "generic/message.html", context={"message": "已经超过24小时，链接失效"})
        except BadSignature:
            return render(request, "generic/message.html", context={"message": "您使用的为非法链接，可能经过篡改"})
        else:
            username = res['username']
            User.objects.filter(username=username).update(is_active=1)
            return render(request, "generic/message.html", context={"message": "您的账号已激活"})
