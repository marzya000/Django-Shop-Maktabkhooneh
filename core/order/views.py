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
from django.urls import reverse_lazy,reverse
from cart.cart import CartSession
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from payment.clients.zarinpal_client import ZarinPalSandbox
from payment.clients.zibal_client import ZibalClient
from payment.clients.payexa_client import PayexaClient
from payment.models import PaymentModel




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

            order.coupon = coupon
            coupon.used_by.add(self.request.user)
            coupon.save()

        order.total_price = total_price
        order.save()
        ### انتخاب درگاه اصلی پی اکسا # یا زیبال  یا # زرین‌پال
        return redirect(self.create_payment_url(order))
    

    def create_payment_url(self,order):
        zarinpal = ZarinPalSandbox()
        
        callback_url = self.request.build_absolute_uri(
            reverse("payment:verify")
        )
        
        response = zarinpal.payment_request(order.get_price(),callback_url=callback_url,
        description=f"پرداخت سفارش {order.id}",
        )
        authority = response['data']['authority']

        payment_obj = PaymentModel.objects.create(
            authority_id = authority,          
            amount = order.get_price(),
        )
        order.payment = payment_obj
        order.save()
        return zarinpal.generate_payment_url(authority)


    def create_zibal_payment_url(self, order):
        zibal = ZibalClient(merchant="zibal")

        callback_url = self.request.build_absolute_uri(
            reverse("payment:zibal_verify")
        )

        response = zibal.payment_request(
            order.get_price(),
            callback_url=callback_url,
            description=f"پرداخت سفارش {order.id}",
        )

        track_id = response["trackId"]

        payment_obj = PaymentModel.objects.create(
            authority_id=str(track_id),
            amount=order.get_price(),
        )

        order.payment = payment_obj
        order.save()

        return zibal.generate_payment_url(track_id)


    def create_payexa_payment_url(self, order):
        payexa = PayexaClient()

        callback_url = self.request.build_absolute_uri(
            reverse("payment:payexa_verify")
        )
        response = payexa.payment_request(
            amount=order.get_price(),
            callback_url=callback_url,
            order_ref=order.id,
        )

        payment_obj = PaymentModel.objects.create(
            authority_id= response["authority"],
            amount= order.get_price(),
            response_json= response,
        )

        order.payment = payment_obj
        order.save()
        return payexa.generate_payment_url(
            response["authority"]
        )

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

class OrderFailedView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name = 'order/failed.html'


class ValidateCouponView(LoginRequiredMixin,HasCustomerAccessPermission,View):

    def post(self,request,*args,**kwargs):
        code = request.POST.get("code")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت ثبت شد"
        total_price = 0
        total_tax = 0
        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message":"کد تخفیف یافت نشد"},status=404)
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code,message = 403,"محدودیت در تعداد استفاده"
        
            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code,message = 403,"کد تخفیف منقضی شده است"
        
            elif user in coupon.used_by.all():
                status_code,message = 403,"این کد تخفیف قبلا توسط شما استفاده شده است"

            else:
                cart = CartModel.objects.get(user=self.request.user)
                total_price = cart.calculate_total_price()
                total_price = round(total_price - (total_price * (coupon.discount_percent/100)))
                total_tax = round((total_price * 9)/100)

        return JsonResponse({"message":message,"total_tax":total_tax,"total_price":total_price},status=status_code)