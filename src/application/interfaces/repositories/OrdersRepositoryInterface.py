from abc import abstractmethod, ABC
from typing import List
from src.domain.entities import OrderEntity
from .. import FiltersExpression


class OrdersRepositoryInterface(ABC):

    @abstractmethod
    async def store_orders(self, orders: List[OrderEntity]) -> None:
        """
        Store in database the fetched orders
        :param orders:
        :return:
        """
        pass

    @abstractmethod
    async def fetch_orders(self, filters: FiltersExpression,
                           **kwargs) -> List[OrderEntity]:
        """
        Get orders stored
        :param filters:
        :param kwargs:
        :return:
        """
        pass
