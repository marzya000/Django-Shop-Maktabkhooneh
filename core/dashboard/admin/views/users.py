from django.views.generic import (
    UpdateView,
    ListView,
    DeleteView,  
) 
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import FieldError
from django.db.models import F,Q
from accounts.models import UserType
from django.contrib.auth import get_user_model
User = get_user_model()



class UserListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name = 'dashboard/admin/users/user-list.html'    
    paginate_by = 1
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)           

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False,type=UserType.customer.value).order_by('-created_date')
        
        if search_q:=self.request.GET.get('q'):
            queryset = queryset.filter(Q(email__icontains=search_q))
        if order_by:= self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['total_result'] = self.get_queryset().count()
        # self.request.session['fav_color'] = 'blue'       
        return context


class UserUpdateView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):    
    template_name = 'dashboard/admin/users/user-edit.html'
    form_class = UserForm
    success_message = "کاربر موردنظر با موفقیت ویرایش شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:user-edit",kwargs={"pk":self.get_object().pk})

    def get_queryset(self):
        return User.objects.filter(is_superuser=False,type=UserType.customer.value)



class UserDeleteView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,DeleteView):
    template_name = 'dashboard/admin/users/user-delete.html'
    success_url = reverse_lazy("dashboard:admin:user-list")
    success_message = "حذف کاربر با موفقیت انجام شد"

    def get_queryset(self):
        return User.objects.filter(is_superuser=False,type=UserType.customer.value)
