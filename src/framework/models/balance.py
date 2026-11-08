from decimal import Decimal

from pydantic import BaseModel


class Balance(BaseModel):
    asset: str
    available: Decimal
    locked: Decimal
