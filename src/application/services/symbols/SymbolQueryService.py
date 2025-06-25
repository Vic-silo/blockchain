from asyncio import gather

from .SymbolService import SymbolService
from ..orders import OrderQueryService
from src.core import logger
from src.core.enums import OrderType
from src.domain.entities import SymbolOrderStatsEntity, SymbolWholeStatsEntity, OrderEntity
from src.exceptions import UnknownSymbolException
from typing import List
from ...interfaces import FiltersExpression


class SymbolQueryService(SymbolService):

    async def validate_symbol(self, symbol: str):
        symbols = await self.fetch_symbols()
        if symbol not in symbols:
            logger.error(f'Unknown symbol: {symbol}.\tExpected: {symbols}')
            raise UnknownSymbolException()

    async def fetch_symbols(self) -> List[str]:
        symbols = await self.repository.fetch_symbols()
        return await self.entity.fetch_symbols(symbols=symbols)

    async def fetch_symbol_stats_by_order_type(
            self,
            symbol: str, order_type: str,
            order_service: OrderQueryService) -> SymbolOrderStatsEntity:
        await self.validate_symbol(symbol=symbol)
        order_type = OrderType(order_type)
        # Fetch from database symbol stats by order
        filters = FiltersExpression(
            filter_exp='order_type=order_type AND symbol=symbol',
            filter_val={"order_type": order_type.value, "symbol": symbol}
        )
        orders = await order_service.fetch_order(filters=filters)
        return await SymbolOrderStatsEntity.create(
            symbol=symbol, order_type=order_type, orders=orders)

    async def fetch_symbol_stats_whole(
            self,
            order_service: OrderQueryService) -> SymbolWholeStatsEntity:
        symbols = await self.fetch_symbols()
        tasks = [self.fetch_whole_orders(symbol=symbol, order_service=order_service)
                 for symbol in symbols]
        orders_per_symbol = await gather(*tasks)
        whole_orders = [order
                        for orders in orders_per_symbol
                        for order in orders]
        return await SymbolWholeStatsEntity.create(orders=whole_orders)

    @staticmethod
    async def fetch_whole_orders(
            symbol: str,
            order_service: OrderQueryService) -> List[OrderEntity]:
        # Fetch from database symbol stats by order
        filters = FiltersExpression(
            filter_exp='symbol=symbol',
            filter_val={"symbol": symbol}
        )
        return await order_service.fetch_order(filters=filters)
