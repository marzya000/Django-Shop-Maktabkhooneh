from django.views.generic import (
    View,
    TemplateView,
    UpdateView,
    ListView,
    DeleteView,
    CreateView
) 
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import FieldError

from django.db.models import F,Q
from accounts.models import UserType,User
from django.contrib.auth import get_user_model
# User = get_user_model()



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

# class AdminProductCreateView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,CreateView):    
#     template_name = 'dashboard/admin/products/product-create.html'
#     queryset = ProductModel.objects.all()
#     form_class = ProductForm
#     success_message = "ایجاد محصول با موفقیت انجام شد"

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         super().form_valid(form)
#         return redirect(reverse_lazy("dashboard:admin:product-edit",kwargs={"pk": form.instance.pk}))
    
#     def get_success_url(self):
#         return reverse_lazy("dashboard:admin:product-list")



# class AdminProductEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):    
#     template_name = 'dashboard/admin/products/product-edit.html'
#     queryset = ProductModel.objects.all()
#     form_class = ProductForm
#     success_message = "ویرایش محصول با موفقیت انجام شد"

#     def get_success_url(self):
#         return reverse_lazy("dashboard:admin:product-edit",kwargs={"pk":self.get_object().pk})



# class AdminProductDeleteView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,DeleteView):
#     template_name = 'dashboard/admin/products/product-delete.html'
#     queryset = ProductModel.objects.all()
#     success_url = reverse_lazy("dashboard:admin:product-list")
#     success_message = "حذف محصول با موفقیت انجام شد"
