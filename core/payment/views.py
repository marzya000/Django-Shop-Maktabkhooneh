from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel,OrderStatusType


class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")
        payment_obj = get_object_or_404(PaymentModel,authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)

       # اگر کاربر پرداخت را لغو کرده باشد
        if status != "OK":            
            payment_obj.response_code = None
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = { "callback_status": status, "authority": authority_id }
            payment_obj.save()
            order.status = OrderStatusType.failed.value
            order.save()
            return redirect(reverse_lazy('order:failed'))
        
        # Verify payment
        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify( int(payment_obj.amount), payment_obj.authority_id )

        # اطلاعات اصلی پاسخ Verify
        data = response.get("data", {}) 
        response_code = data.get("code") 
        ref_id = data.get("ref_id")
        payment_obj.response_code = response_code
        payment_obj.response_json = response 
        # پرداخت موفق
        if response_code in [100, 101]:
            payment_obj.ref_id = ref_id
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.save()
            
            order.status = OrderStatusType.success.value
            order.save()
            return redirect(reverse_lazy("order:completed"))

        # پرداخت ناموفق
        payment_obj.status = PaymentStatusType.failed.value
        payment_obj.save()
        
        return redirect(reverse_lazy("order:failed"))