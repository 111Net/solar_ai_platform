import requests
from .base import CreditBureauAdapter

class CRCAdapter(CreditBureauAdapter):

    BASE_URL = "https://api.crc.example.com"

    def fetch_credit_report(self, bvn: str):
        response = requests.post(
            f"{self.BASE_URL}/credit-report",
            json={"bvn": bvn},
            headers={"Authorization": "Bearer YOUR_API_KEY"}
        )
        return response.json()