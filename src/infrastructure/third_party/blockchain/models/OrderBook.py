from pydantic import BaseModel, Field
from typing import List
from src.domain.entities import OrderEntity
from src.core.enums import OrderType
from src.core import logger


class _Order(BaseModel):

    px: float = Field(default_factory=float)
    qty: float = Field(default_factory=float)
    num: float = Field(default_factory=float, description="Either the quantity of orders on this price level for L2, or the individual order id for L3")


class OrderBook(BaseModel):

    symbol: str
    bids: List[_Order] = Field(default_factory=list)
    asks: List[_Order] = Field(default_factory=list)

    async def to_entity(self) -> List[OrderEntity]:
        orders = [await OrderEntity.create(
            symbol=self.symbol, order_type=OrderType.BUY, price=order.px, qty=order.qty)
                  for order in self.bids]
        orders.extend([await OrderEntity.create(
            symbol=self.symbol, order_type=OrderType.SELL, price=order.px, qty=order.qty)
                       for order in self.asks])
        logger.debug(f'Total bids: {len(self.bids)}\tTotal asks: {len(self.asks)}'
                     f'\tTotal orders: {len(orders)}')

        return orders
