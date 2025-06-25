from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from src.core.enums import Defaults
from src.core import logger
from src.domain.entities import SymbolEntity
from src.exceptions import SymbolStatusParseException
from traceback import format_exc
from pandas import DataFrame


class SymbolStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    base_currency: Optional[str] = Field(default=Defaults.STR.value, description="Blockchain symbol identifier")
    base_currency_scale: Optional[int] = Field(default=Defaults.DEC.value, description="The number of decimals the currency can be split in")
    counter_currency: Optional[str] = Field(default=Defaults.STR.value, description="Blockchain symbol identifier")
    counter_currency_scale: Optional[int] = Field(default=Defaults.DEC.value, description="The number of decimals the currency can be split in")
    min_price_increment: Optional[int] = Field(default=Defaults.DEC.value, description="The price of the instrument must be a multiple of min_price_increment * (10^-min_price_increment_scale)")
    min_price_increment_scale: Optional[int] = Field(default=Defaults.DEC.value, description="none")
    min_order_size: Optional[int] = Field(default=Defaults.DEC.value, description="The minimum quantity for an order for this instrument must be min_order_size*(10^-min_order_size_scale)")
    min_order_size_scale:  Optional[int] = Field(default=Defaults.DEC.value, description="none")
    max_order_size: Optional[int] = Field(default=Defaults.DEC.value, description="The maximum quantity for an order for this instrument is max_order_size*(10^-max_order_size_scale). If this equal to zero, there is no limit")
    max_order_size_scale:  Optional[int] = Field(default=Defaults.DEC.value, description="none")
    lot_size: Optional[int] = Field(default=Defaults.DEC.value, description="none")
    lot_size_scale:  Optional[int] = Field(default=Defaults.DEC.value, description="none")
    status:  Optional[str] = Field(default=Defaults.STR.value, description="Symbol status; open, close, suspend, halt, halt-freeze.")
    id_symbol: Optional[int] = Field(default=Defaults.DEC.value, description="none", alias="id")
    auction_price:  Optional[float] = Field(default=Defaults.FLOAT.value, description="If the symbol is halted and will open on an auction, this will be the opening price.")
    auction_size:  Optional[float] = Field(default=Defaults.FLOAT.value, description="Opening size")
    auction_time:  Optional[str] = Field(default=Defaults.STR.value, description="Opening time in HHMM format")
    imbalance:  Optional[float] = Field(default=Defaults.FLOAT.value, description="Auction imbalance. If > 0 then there will be buy orders left over at the auction price. If < 0 then there will be sell orders left over at the auction price.")

    @classmethod
    async def to_entity_whole(cls, response: dict) -> List[SymbolEntity]:
        """
        Return the whole SymbolStatus in the blockchain API
        :param response:
        :return:
        """
        # Load and validate each response symbol
        try:
            validated = {k: cls(**v) for k, v in response.items()}

        except Exception:
            logger.error(msg=f'SymbolStatus to entity error: {format_exc()}')
            raise SymbolStatusParseException()

        # Create DF with compound_symbol attribute
        df = DataFrame.from_dict(
            {k: v.model_dump(mode='json') for k, v in validated.items()},
            orient='index'
        ).reset_index().rename(columns={'index': 'compound_symbol'})

        # Dump df into dictionary and return SymbolEntity
        symbols = df.to_dict(orient='records')
        return [SymbolEntity(**symbol) for symbol in symbols]
