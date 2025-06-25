from abc import abstractmethod, ABC
from typing import List
from src.domain.entities import OrderEntity, SymbolEntity


class BlockchainInterface(ABC):

    @abstractmethod
    async def fetch_symbols(self) -> List[SymbolEntity]:
        """
        Fetch from blockchain API all the symbols
        :return:
        """
        pass

    @abstractmethod
    async def fetch_order_book_l3(self, compound_symbol: str) -> List[OrderEntity]:
        """
        Fetch order books level3 data
        :param compound_symbol:
        :return:
        """
        pass
