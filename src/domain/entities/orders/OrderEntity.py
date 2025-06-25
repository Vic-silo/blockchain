from pydantic import BaseModel
from src.core.enums import OrderType
from typing import Optional


class OrderEntity(BaseModel):

    symbol: str
    order_type: OrderType
    px: float
    qty: float
    value: float

    @classmethod
    async def create(cls,
                     symbol: str,
                     order_type: str,
                     price: float,
                     qty: float):
        return cls(
            symbol=symbol,
            order_type=OrderType(order_type),
            px=price, qty=qty, value=price*qty)
