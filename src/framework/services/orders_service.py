from framework.services.base_service import BaseService


class OrdersService(BaseService):
    def create(self, symbol: str, side: str, type: str, price: int, quantity: int):
        data = {"symbol": symbol, "side": side, "type": type, "price": price, "quantity": quantity}

        return self.client.post("/orders", json=data)

    def list(self, status: str | None = None):
        return self.client.get("/orders", params={"status": status})

    def get(self, order_id):
        return self.client.get(f"/orders/{order_id}")

    def cancel(self, order_id):
        return self.client.delete(f"/orders/{order_id}")
