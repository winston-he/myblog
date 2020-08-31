from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from itsdangerous import SignatureExpired, BadSignature

from mail.mail_string import get_activate_msg
from mail.views import send_email
from myblog.settings import EMAIL_FROM
from .forms import UserRegisterForm, PersonalInfoForm
from .models import User, UserProfile, UserPreference
from .utils import generate_token, load_token


class MyLogoutView(LogoutView):
    # def re
    pass


class UpdatePersonalInfoView(LoginRequiredMixin, UpdateView):
    template_name = "profile/personal_info_form.html"
    model = User
    form_class = PersonalInfoForm

    def form_valid(self, form):
        return super().form_valid(form)


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
                             html_message=get_activate_msg(form.cleaned_data['username'],
                                                           "{}/{}/{}".format(host, 'registration/activate',
                                                                             generate_token({"username":
                                                                                                 form.cleaned_data[
                                                                                                     'username']}))),
                             expires=2)
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
