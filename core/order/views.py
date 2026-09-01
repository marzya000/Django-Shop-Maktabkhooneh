from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import HasCustomerAccessPermission
from django.views.generic import (
    TemplateView,
    FormView
)
from django.views import View
from order.models import UserAddressModel,OrderModel,OrderItemModel,CouponModel
from order.forms import CheckOutForm
from cart.models import CartModel
from django.urls import reverse_lazy
from cart.cart import CartSession
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone



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
        coupon = cleaned_data["coupon"]

        cart = CartModel.objects.get(user=self.request.user)
        cart_items = cart.cart_items.all()
        order = OrderModel.objects.create(
            user =self.request.user,
            address = address.address,
            state = address.state,
            city = address.city,
            zip_code =  address.zip_code,       
        )
        for item in cart_items :
            OrderItemModel.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.get_price(),
            )
        cart_items.delete()
        CartSession(self.request.session).clear()
        total_price = order.calculate_total_price()
        if coupon:
            total_price = total_price - round((total_price * Decimal(coupon.discount_percent/100)))
            order.coupon = coupon

            coupon.used_by.add(self.request.user)
            coupon.save()

        order.total_price = total_price
        order.save()

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



class ValidateCouponView(LoginRequiredMixin,HasCustomerAccessPermission,View):

    def post(self,request,*args,**kwargs):
        code = request.POST.get("code")
        user = self.request.user

        is_valid = True
        message = "کد تخفیف با موفقیت ثبت شد"
        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"is_valid":False, "message":"کد تخفیف یافت نشد"})
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                is_valid,message = False,"محدودیت در تعداد استفاده"
        
            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                is_valid,message = False,"کد تخفیف منقضی شده است"
        
            if user in coupon.used_by.all():
                is_valid,message = False,"این کد تخفیف قبلا توسط شما استفاده شده است"

        return JsonResponse({"is_valid":is_valid, "message":message})