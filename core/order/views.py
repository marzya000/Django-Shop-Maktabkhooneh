from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import HasCustomerAccessPermission
from django.views.generic import (
    TemplateView,
    FormView
)
from order.models import UserAddressModel
from order.forms import CheckOutForm
from cart.models import CartModel
from django.urls import reverse_lazy

class OrderCheckOutView(LoginRequiredMixin,HasCustomerAccessPermission,FormView):
    template_name = 'order/checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('order:completed')

    def get_form_kwargs(self):
        kwargs = super(OrderCheckOutView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
    

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        address = cleaned_data["address_id"]
        print(address)

        # print(self.request.POST) 
        return super().form_valid(form)

    def form_invalid(self, form):
        print(self.request.POST)         
        return super().form_invalid(form)
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user)
        context["addresses"] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price * 9)/100)
        return context

class OrderCompletedView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = 'order/completed.html'