from pydantic import BaseModel
from typing import List
from pandas import DataFrame, Series
from src.core.enums import OrderType
from ..orders import OrderEntity


class SymbolOrderStatsEntity(BaseModel):
    """Stats for a symbol and given OrderType
    """

    symbol: str
    order_type: OrderType
    average_value: float
    grater_value: OrderEntity
    lesser_value: OrderEntity
    total_qty: float
    total_orders: int

    @classmethod
    async def create(cls,
                     symbol: str,
                     order_type: OrderType,
                     orders: List[OrderEntity]) -> 'SymbolOrderStatsEntity':
        orders_df = DataFrame([_.model_dump(mode='json') for _ in orders])

        avg_value = orders_df["value"].mean()
        total_qty = orders_df["qty"].sum()
        total_orders = Series(orders_df.to_dict()).size
        grater_value = orders_df.loc[orders_df["value"].idxmax()]
        lesser_value = orders_df.loc[orders_df["value"].idxmin()]

        return cls(
            symbol=symbol,
            order_type=order_type,
            average_value=avg_value,
            grater_value=grater_value,
            lesser_value=lesser_value,
            total_qty=total_qty,
            total_orders=total_orders)
