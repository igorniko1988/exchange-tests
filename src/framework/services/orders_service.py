from framework.models.orders import CreateOrderRequest
from framework.services.base_service import BaseService


class OrdersService(BaseService):
    def create(self, order: CreateOrderRequest):
        body = order.model_dump(mode="json", exclude_none=True)
        return self.client.post("/orders", json=body)

    def list(self, status: str | None = None):
        return self.client.get("/orders", params={"status": status})

    def get(self, order_id):
        return self.client.get(f"/orders/{order_id}")

    def cancel(self, order_id):
        return self.client.delete(f"/orders/{order_id}")
