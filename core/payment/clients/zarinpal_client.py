import requests
import json
from django.conf import settings

class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    
    _callback_url = "http://127.0.0.1:8000/payment/verify"



    def __init__(self,merchant_id=None):
        self.merchant_id = merchant_id or settings.MERCHANT_ID

    def payment_request(self, amount, callback_url=None, description="پرداختی کاربر"):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "callback_url": callback_url or self._callback_url,
            "description": description,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        response = requests.post(
            self._payment_request_url, headers=headers, json=payload,
        timeout=15)

        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            raise Exception(f"ZarinPal Error: {data['errors']}")
        return data

    def payment_verify(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "authority": authority,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        response = requests.post(
            self._payment_verify_url, headers=headers, json=payload,
        timeout=15)

        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            raise Exception(f"ZarinPal Error: {data['errors']}")
        return data

    def generate_payment_url(self, authority):
        return self._payment_page_url + authority

