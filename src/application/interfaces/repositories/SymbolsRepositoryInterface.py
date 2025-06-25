from abc import abstractmethod, ABC
from typing import List
from src.domain.entities import SymbolEntity
from src.application.interfaces import FiltersExpression


class SymbolsRepositoryInterface(ABC):

    @abstractmethod
    async def store_symbols(self, symbols: List[SymbolEntity]) -> None:
        """
        Store in database the available symbols
        :param symbols:
        :return:
        """
        pass

    @abstractmethod
    async def fetch_symbols(self,
                            filters: FiltersExpression = None,
                            **kwargs) -> List[SymbolEntity]:
        """
        Fetch from storage the available symbols
        :param filters:
        :param kwargs:
        :return:
        """
        pass
