# Create your views here.
from django.http import JsonResponse
from django.views.generic import TemplateView


# class IndexView(TemplateView):
#     template_name = 'room/index.html'


class ChatRoomView(TemplateView):
    template_name = 'chat/chat.html'

    # def get_context_data(self, **kwargs):
    #     pass


# 更新签名
def update_signature(request):
    new_sign = request.POST.get("new_sign")
    if new_sign is None:
        return JsonResponse({"result": -1, "msg": "错误的参数"})

    request.user.chat_info.signature = new_sign
    request.user.chat_info.save()
    return JsonResponse({"result": 1, "msg": "OK"})