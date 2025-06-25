from .OrderService import OrderService
from ...interfaces import FiltersExpression
from typing import List
from src.domain.entities import OrderEntity


class OrderQueryService(OrderService):

    async def fetch_order(self, filters: FiltersExpression) -> List[OrderEntity]:
        # Get from database the orders filtered
        return await self.repository.fetch_orders(filters=filters)
