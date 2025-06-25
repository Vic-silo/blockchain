from src.application.interfaces import OrdersRepositoryInterface, FiltersExpression
from .BaseMongoRepository import BaseMongoRepository
from typing import List
from src.domain.entities import OrderEntity
from .models import OrderMongoModel
from src.exceptions import NotElementsFoundException
from src.core import logger


class OrdersRepositoryAdapter(BaseMongoRepository, OrdersRepositoryInterface):

    COLLECTION_NAME = 'orders'

    async def store_orders(self, orders: List[OrderEntity]) -> None:
        orders_db = []
        for order in orders:
            order_db = await OrderMongoModel.from_entity(order=order)
            orders_db.append(order_db.model_dump())

        await self.add_many(documents=orders_db)

    async def fetch_orders(self,
                           filters: FiltersExpression,
                           **kwargs) -> List[OrderEntity]:
        if filters:
            filters = self.parse_filter_expr(expr=filters.filter_exp,
                                             values=filters.filter_val)
        else:
            filters = {}
        orders = await self.select_data(filters=filters, return_all=True)
        if not orders:
            logger.warning(f'Not found orders for filters: {filters}')
            raise NotElementsFoundException()
        return [await OrderMongoModel(**order).to_entity()
                for order in orders]

