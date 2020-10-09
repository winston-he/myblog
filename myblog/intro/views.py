from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import TemplateView


class IntroductionView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = self.get_context_data(**kwargs)
            s = render_to_string('home/homepage.html', context=context)
            return HttpResponse(content=s, content_type="text/html")
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post = {
            'author': User.objects.filter(pk=1).first()
        }
        kwargs['post'] = post
        return super().get_context_data(**kwargs)

