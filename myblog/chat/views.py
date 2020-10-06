# Create your views here.
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django_redis import get_redis_connection
# class IndexView(TemplateView):
#     template_name = 'room/index.html'
from chat.chat_user import add_chat_user
from chat.decorators import webim_token_check
from chat.models import PrivateChatRecord


class ChatRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        target = self.request.GET.get('target')
        if target == 'true':
            target_user = self.request.GET.get('talk_to')
            add_chat_user(self.request.user.username, target_user)

            # 增加私聊记录
            talk_to = User.objects.filter(username=target_user).first()
            if not (PrivateChatRecord.objects.filter(Q(user_1=self.request.user) & Q(user_2=talk_to)).first() or
                    PrivateChatRecord.objects.filter(Q(user_1=talk_to) & Q(user_2=self.request.user)).first()):
                PrivateChatRecord(user_1=self.request.user, user_2=talk_to).save()
            context['target'] = True
            context['target_user'] = target_user
        else:
            context['target'] = False
        return self.render_to_response(context)


class ChatListView(LoginRequiredMixin, ListView):
    """
    与前端LayIM配合使用的聊天历史记录列表
    """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            friends, private_chat_list = [], []
            records = self.get_queryset()
            friends.append(
                {
                    "groupname": "私信",
                    "id": 0,
                    "list": private_chat_list
                }
            )
            for record in records:
                friend = record.user_1 if record.user_2 == self.request.user else record.user_2
                private_chat_list.append({
                    "username": friend.username,
                    "id": friend.username,
                    "avatar": reverse("profile_image"),
                    "sign": "Hello World",
                    "status": "online"  # default setting
                })

            return JsonResponse({"result": 0, "friends": friends})

        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return PrivateChatRecord.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user)).all()


@webim_token_check
def get_chat_token(request, token):
    return JsonResponse({"token": token, "result": 0})

def webim_info(request):
    conn = get_redis_connection("default")

    res = conn.hgetall('webim_info')

    return JsonResponse(res)


# 更新签名
def update_signature(request):
    new_sign = request.POST.get("new_sign")
    if new_sign is None:
        return JsonResponse({"result": -1, "msg": "错误的参数"})

    request.user.chat_info.signature = new_sign
    request.user.chat_info.save()
    return JsonResponse({"result": 1, "msg": "OK"})
