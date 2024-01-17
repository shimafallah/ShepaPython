import requests

class ShepaPayment:
    API_VERSION = 'v1'

    def __init__(self, api, sandbox=True):
        self.api = api
        self.baseURL = f'https://{"sandbox." if sandbox else ""}shepa.com/api/{self.API_VERSION}'
        self.headers = {
            'Content-Type': 'application/json',
        }

    def _post_request(self, endpoint, data):
        url = f'{self.baseURL}/{endpoint}'
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_payment(self, amount, callback, mobile=None, email=None, description=None):
        data = {
            'api': self.api,
            'amount': amount,
            'callback': callback,
            'mobile': mobile,
            'email': email,
            'description': description,
        }
        return self._post_request('token', data)

    def verify_payment(self, token, amount):
        data = {
            'api': self.api,
            'token': token,
            'amount': amount,
        }
        return self._post_request('verify', data)

    def refund_payment(self, amount, transaction_id):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number.")
        
        if not transaction_id:
            raise ValueError("Transaction ID is required for refund.")

        data = {
            'api': self.api,
            'amount': amount,
            'transaction_id': transaction_id,
        }
        return self._post_request('refund-transaction', data)
