from django.shortcuts import redirect
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from accounts.models import UserType
# Create your views here.

class CustomerDashboardHomeView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/customer/home.html"