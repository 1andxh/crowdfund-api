import httpx
from typing import Any
from src.config import config

PAYSTACK_SECRET_KEY = config.PAYSTACK_SECRET_KEY
PAYSTACK_BASE_URL = config.PAYSTACK_BASE_URL


class PaystackClient:
    def __init__(self):
        self.secret_key = PAYSTACK_SECRET_KEY
        self.base_url = PAYSTACK_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    async def intialize_transcation(
        self, email: str, amount: float, reference: str, callback_url: str | None = None
    ) -> dict[str, Any]:
        """initialize a transaction"""

        amount_in_pesewas = int(amount * 100)

        payload = {
            "email": email,
            "amount": amount_in_pesewas,
            "reference": reference,
            "currency": "GHS",
        }
        if callback_url:
            payload["callback_url"] = callback_url

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()

            data = response.json()

            if data.get("status"):
                return data["data"]
            else:
                raise Exception(f"Paystack error: {data.get("message")}")
