import requests
from django.conf import settings

class IDPayClient:
    _payment_request_url = "https://api.idpay.ir/v1.1/payment"
    _payment_verify_url = "https://api.idpay.ir/v1.1/payment/verify"
    _payment_page_url = "https://idpay.ir/p/ws-sandbox/"
    _callback_url = "http://127.0.0.1:8000/payment/verify"



    def __init__(self, api_key=None, sandbox=True):
        self.api_key = api_key or settings.IDPAY_API_KEY
        self.sandbox = sandbox

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

        if self.sandbox:
            headers["X-SANDBOX"] = "1"

        return headers

    def payment_request(self, order_id, amount, callback_url=None, description="پرداختی کاربر"):
        payload = {
            "order_id": str(order_id),
            "amount": int(amount),
            "callback_url": callback_url or self._callback_url,
            "desc": description,
        }

        response = requests.post(self._payment_request_url, headers=self._get_headers(), json=payload,
                timeout=15)

        print("-" * 50)
        print("IDPAY REQUEST")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("-" * 50)

        response.raise_for_status()
        data = response.json()
        if "error_code" in data:
            raise Exception(
                f"IDPay Error: {data.get('error_message')}"
            )
        return data


    def payment_verify(self, payment_id, order_id):
        payload = {
            "id": payment_id,
            "order_id": str(order_id),
        }
        response = requests.post(self._payment_verify_url, headers=self._get_headers(), json=payload,
                        timeout=15)

        print("-" * 50)
        print("IDPAY VERIFY")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("-" * 50)

        response.raise_for_status()
        data = response.json()
        if "error_code" in data:
            raise Exception(
                f"IDPay Error: {data.get('error_message')}"
            )
        return data


    def generate_payment_url(self, payment_id):
        return self._payment_page_url + payment_id
               
        