from decimal import Decimal

from framework.services.base_service import BaseService


class BalancesService(BaseService):
    def list(self):
        return self.client.get("/balances")

    def deposit(self, asset: str, amount: int | Decimal):
        data = {"asset": asset, "amount": str(amount)}
        return self.client.post("/balances/deposit", json=data)
