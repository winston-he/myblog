from django.shortcuts import render
from django.views.generic import CreateView
from .forms import UserForm

# Create your views here.
class CreateUserView(CreateView):
    form_class = UserForm
    template_name = 'user_form.html'
