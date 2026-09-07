import requests
from django.conf import settings


class ZibalClient:

    _payment_request_url = "https://gateway.zibal.ir/v1/request"
    _payment_verify_url = "https://gateway.zibal.ir/v1/verify"
    _payment_page_url = "https://gateway.zibal.ir/start/"

    _callback_url = "http://127.0.0.1:8000/payment/zibal/verify"

    def __init__(self, merchant=None):
        self.merchant = merchant or settings.ZIBAL_MERCHANT

    def payment_request(
        self,
        amount,
        callback_url=None,
        description="پرداختی کاربر"
    ):
        payload = {
            "merchant": self.merchant,
            "amount": int(amount),
            "callbackUrl": callback_url or self._callback_url,
            "description": description,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(
            self._payment_request_url,
            headers=headers,
            json=payload,
            timeout=15
        )

        print("-" * 50)
        print("ZIBAL REQUEST")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("-" * 50)

        response.raise_for_status()

        data = response.json()

        if data.get("result") != 100:
            raise Exception(f"Zibal Error: {data.get('message')}")

        return data

    def generate_payment_url(self, track_id):
        return self._payment_page_url + str(track_id)


    def payment_verify(self, track_id):

        payload = {
            "merchant": self.merchant,
            "trackId": int(track_id),
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(
            self._payment_verify_url,
            headers=headers,
            json=payload,
            timeout=15
        )

        print("-" * 50)
        print("ZIBAL VERIFY")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("-" * 50)

        response.raise_for_status()

        data = response.json()

        if data.get("result") not in [100, 201]:
            raise Exception(
                f"Zibal Error: {data.get('message')}"
            )

        return data


if __name__ == "__main__":

    zibal = ZibalClient(
        merchant="zibal"
    )

    track_id = "4774691693"

    response = zibal.payment_verify(track_id)

    print(response)

    # response = zibal.payment_request(
    #     amount=15000,
    #     description="تست پرداخت"
    # )

    # print(response)

    # track_id = response["trackId"]

    # payment_url = zibal.generate_payment_url(track_id)

    # print("PAYMENT URL:", payment_url)