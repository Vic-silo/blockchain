from .OrderService import OrderService
from ..symbols import SymbolQueryService
from asyncio import gather


class OrderCreateService(OrderService):

    async def store_order(self,
                          symbol: str,
                          symbol_service: SymbolQueryService) -> None:
        """
        Get the orders from third-party and store them in database for further
        queries
        :param symbol:
        :param symbol_service:
        :return:
        """
        # Validate the symbol input
        await symbol_service.validate_symbol(symbol=symbol)

        # Get from third_party the order by symbol
        symbol_orders = await self.order_api.fetch_order_book_l3(
            compound_symbol=symbol)
        # Store in database the orders
        await self.repository.store_orders(orders=symbol_orders)

    async def store_whole_orders(self,
                                 symbol_service: SymbolQueryService) -> None:
        """
        Iterate over all the symbols and store its orders in database
        :param symbol_service:
        :return:
        """
        symbols = await symbol_service.fetch_symbols()
        tasks = [self.store_order(symbol=symbol, symbol_service=symbol_service)
                 for symbol in symbols]
        await gather(*tasks)
