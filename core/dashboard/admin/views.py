from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import AdminPasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name = "dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name = "dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "بروزرسانی پسورد با موفقیت انجام شد"
    