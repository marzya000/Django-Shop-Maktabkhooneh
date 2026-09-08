import requests
from django.conf import settings


class PayexaClient:

    _payment_request_url = "https://sandbox.pexn.ir/v1/payment/request"
    _payment_verify_url = "https://sandbox.pexn.ir/v1/payment/verify"
    _payment_page_url = "https://sandbox.pexn.ir/startPay?authority="

    _callback_url = "http://127.0.0.1:8000/payment/payexa/verify"

    def __init__(self, api_key=None):
        self.api_key = api_key or settings.PAYEXA_API_KEY


    def payment_request(self, amount, callback_url=None, order_ref=None):
        payload = {
            "amount": int(amount),
            "callback_url": callback_url or self._callback_url,
            "meta": {
                "order_ref": str(order_ref) if order_ref else None,
            }
        }
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key, 
        }

        response = requests.post(
            self._payment_request_url,
            headers=headers,
            json=payload,
            timeout=10
            )        


        response.raise_for_status()

        data = response.json()

        if "authority" not in data:
            raise Exception(f"payexa Error: {data}")

        return data


    def generate_payment_url(self, authority):
        return self._payment_page_url + str(authority)

    def payment_verify(self, order_id, token):

        payload = {
            "order_id": str(order_id),
            "token": str(token),
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key, 
        }

        response = requests.post(
            self._payment_verify_url,
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        return response.status_code, data


if __name__ == "__main__":
    payexa = PayexaClient()

    response = payexa.payment_request(
        amount=15000,
        order_ref="test-001",
        callback_url="http://127.0.0.1:8000/payment/payexa/verify",
        )
    print(response)

