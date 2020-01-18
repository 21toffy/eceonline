from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from user.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,DetailView,View





class HomeView(TemplateView):
    template_name = 'university/homepage.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     category = Category.objects.all()
    #     context['category'] = category
    #     return context
def index(request):
    return redirect (request, 'university/homepage.html')

















