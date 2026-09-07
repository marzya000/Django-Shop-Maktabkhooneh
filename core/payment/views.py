from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from payment.clients.zarinpal_client import ZarinPalSandbox
from payment.clients.zibal_client import ZibalClient
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
        response = zarin_pal.payment_verify( int(payment_obj.amount), payment_obj.authority_id)

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


class ZibalPaymentVerifyView(View):

    def get(self, request, *args, **kwargs):

        success = request.GET.get("success")
        status = request.GET.get("status")
        track_id = request.GET.get("trackId")

        print("-" * 50)
        print("ZIBAL CALLBACK")
        print("SUCCESS:", success)
        print("STATUS:", status)
        print("TRACK ID:", track_id)
        print("-" * 50)

        if not track_id:
            return redirect(reverse_lazy("order:failed"))

        payment_obj = get_object_or_404(
            PaymentModel,
            authority_id=track_id
        )

        order = OrderModel.objects.get(payment=payment_obj)

        if payment_obj.status in [
            PaymentStatusType.success.value,
            PaymentStatusType.failed.value,
        ]:
            if payment_obj.status == PaymentStatusType.success.value:
                return redirect(reverse_lazy("order:completed"))

            return redirect(reverse_lazy("order:failed"))

        # کاربر پرداخت را لغو کرده یا پرداخت موفق نبوده
        if success != "1":
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = {
                "callback_success": success,
                "callback_status": status,
                "trackId": track_id,
            }
            payment_obj.save()

            order.status = OrderStatusType.failed.value
            order.save()

            return redirect(reverse_lazy("order:failed"))

        # Verify payment
        zibal = ZibalClient(merchant="zibal")

        try:
            response = zibal.payment_verify(track_id)

        except Exception as e:

            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = {
                "error": str(e)
            }
            payment_obj.save()

            order.status = OrderStatusType.failed.value
            order.save()

            return redirect(reverse_lazy("order:failed"))

        # ذخیره پاسخ Verify
        payment_obj.response_json = response
        payment_obj.response_code = response.get("result")

        # پرداخت موفق
        if response.get("result") == 100:

            payment_obj.ref_id = response.get("refNumber")
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.save()

            order.status = OrderStatusType.success.value
            order.save()

            return redirect(
                reverse_lazy("order:completed")
            )

        # پرداخت ناموفق
        payment_obj.status = PaymentStatusType.failed.value
        payment_obj.save()

        order.status = OrderStatusType.failed.value
        order.save()

        return redirect(
            reverse_lazy("order:failed")
        )