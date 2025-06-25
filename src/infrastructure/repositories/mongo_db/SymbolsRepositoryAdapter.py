from src.application.interfaces import SymbolsRepositoryInterface, FiltersExpression
from .BaseMongoRepository import BaseMongoRepository
from typing import List
from src.domain.entities import SymbolEntity
from .models import SymbolMongoModel


class SymbolsRepositoryAdapter(BaseMongoRepository, SymbolsRepositoryInterface):

    COLLECTION_NAME = 'symbols'

    async def store_symbols(self, symbols: List[SymbolEntity]) -> None:
        symbols_db = []
        for symbol in symbols:
            symbol_db = await SymbolMongoModel.from_entity(symbol=symbol)
            symbols_db.append(symbol_db.model_dump())

        await self.add_many(documents=symbols_db)

    async def fetch_symbols(self,
                            filters: FiltersExpression = None,
                            **kwargs) -> List[SymbolEntity]:
        if filters:
            filters = self.parse_filter_expr(
                expr=filters.filter_exp, values=filters.filter_val)
        else:
            filters = {}

        symbols = await self.select_data(filters=filters, return_all=True)
        return [await SymbolMongoModel.to_entity(symbol=symbol)
                for symbol in symbols]
