from pydantic import BaseModel, Field, RootModel
from typing import List, Dict
from pandas import DataFrame
from src.core.enums import OrderType
from ..orders import OrderEntity
from src.core import logger


class OrderTypeStats(BaseModel):
    count: int = Field(default=-1)
    qty: float = Field(default=-1.1, description="Number of coins")
    value: float = Field(default=-1.1)

    @classmethod
    async def create(cls, orders_df: DataFrame) -> 'OrderTypeStats':
        logger.debug(f'\n{orders_df}')
        count = orders_df.shape[0]
        qty = orders_df["qty"].sum() if not orders_df.empty else 0.0
        value = orders_df["value"].sum() if not orders_df.empty else 0.0

        return cls(count=count, qty=qty, value=value)


class SymbolStatsEntity(BaseModel):
    bids: OrderTypeStats = Field(default_factory=OrderTypeStats)
    asks: OrderTypeStats = Field(default_factory=OrderTypeStats)


class SymbolWholeStatsEntity(RootModel[Dict[str, SymbolStatsEntity]]):
    """
    Stats for a symbol and all the OrderTypes
    """

    @classmethod
    async def create(cls, orders: List[OrderEntity]) -> 'SymbolWholeStatsEntity':

        df = DataFrame([_.model_dump(mode='json') for _ in orders])
        if df.empty:
            return cls()
        stats = {}
        logger.debug(f'Whole orders df:\n{df}')
        for symbol in df["symbol"].unique():
            symbol_df = df[df["symbol"] == symbol]
            bids_df = symbol_df[symbol_df["order_type"] == OrderType.BUY.value]
            asks_df = symbol_df[symbol_df["order_type"] == OrderType.SELL.value]
            bids = await OrderTypeStats.create(orders_df=bids_df)
            asks = await OrderTypeStats.create(orders_df=asks_df)
            stats[symbol] = SymbolStatsEntity(bids=bids, asks=asks)
        return cls(stats)
