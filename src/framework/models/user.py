from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    created_at: datetime


class UserMe(BaseModel):
    id: str
    email: str
    display_name: str | None
    role: Literal["admin", "user"]
    created_at: datetime
