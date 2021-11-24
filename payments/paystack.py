from decouple import config
import requests as req


class Paystack:
    def __init__(self, reference, *args, **kwargs) -> None:
        PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
        PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
        headers = {
            "Authorization": "Bearer {}".format(PAYSTACK_SECRET_KEY),
            "Content-Type":"application/json",
            "Cache-Control": "no-cache",
        }
        self.reference = reference
        base_url = f"https://api.paystack.co/transaction/verify/{self.reference}"
        self.response = req.get(base_url, headers = headers)
        

    def verify_payment(self):
        if self.response.status_code == 200:
            response_data = self.response.json()
        else:
            return 'Faild.'
        return response_data