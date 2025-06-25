from pydantic import BaseModel, Field
from typing import Optional, List
from src.core.enums import Defaults
from src.exceptions import EmptySymbolException


class SymbolEntity(BaseModel):

    id_symbol: int = Field(description="ID for the symbol")
    compound_symbol: str = Field(description="Compound name crypto-currency")
    base_currency: Optional[str] = Field(default=Defaults.STR.value, description="Blockchain symbol identifier")
    base_currency_scale: Optional[int] = Field(default=Defaults.DEC.value, description="The number of decimals the currency can be split in")
    counter_currency: Optional[str] = Field(default=Defaults.STR.value, description="Blockchain symbol identifier")
    counter_currency_scale: Optional[int] = Field(default=Defaults.DEC.value, description="The number of decimals the currency can be split in")
    status:  Optional[str] = Field(default=Defaults.STR.value, description="Symbol status; open, close, suspend, halt, halt-freeze.")

    @classmethod
    async def fetch_symbols(cls, symbols: List['SymbolEntity']) -> List[str]:
        """
        Get the available symbols in database
        :return:
        """
        if not symbols:
            raise EmptySymbolException()
        symbols = [symbol.compound_symbol for symbol in symbols]
        symbols.sort()
        return symbols
