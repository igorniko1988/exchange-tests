import random
import uuid
from decimal import Decimal

from framework.models.orders import CreateOrderRequest


def unique_email():
    return f"user{uuid.uuid4().hex[:8]}@mail.com"


def credentials():
    return {"email": unique_email(), "password": uuid.uuid4().hex[:12]}


def make_order(**overrides) -> CreateOrderRequest:
    values = {
        "symbol": "BTC-USDT",
        "side": "SELL",
        "type": "LIMIT",
        "price": Decimal(random.randint(1, 100)),
        "quantity": Decimal(random.randint(1, 100)),
    }
    values.update(overrides)
    return CreateOrderRequest(**values)
