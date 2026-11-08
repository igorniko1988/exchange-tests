from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    symbol: Literal["BTC-USDT", "ETH-USDT"] = "BTC-USDT"
    side: Literal["BUY", "SELL"] = "SELL"
    type: Literal["LIMIT", "MARKET"] = "LIMIT"
    price: Decimal | None = Decimal(23)
    quantity: Decimal = Decimal(1)


class Order(BaseModel):
    id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    type: Literal["LIMIT", "MARKET"]
    price: Decimal
    quantity: Decimal
    filled_quantity: Decimal
    status: Literal["NEW", "PARTIALLY_FILLED", "FILLED", "CANCELED"]
    created_at: datetime
    updated_at: datetime
