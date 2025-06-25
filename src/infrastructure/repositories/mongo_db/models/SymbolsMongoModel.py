from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Annotated, Optional
from src.domain.entities import SymbolEntity

PyObjectId = Annotated[str, BeforeValidator(str)]


class SymbolMongoModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias='_id', default=None)
    id_symbol: int
    compound_symbol: str
    base_currency: Optional[str] = Field(default=None)
    base_currency_scale: Optional[int] = Field(default=None)
    counter_currency: Optional[str] = Field(default=None)
    counter_currency_scale: Optional[int] = Field(default=None)
    status: Optional[str] = Field(default=None)

    @classmethod
    async def from_entity(cls, symbol: SymbolEntity) -> 'SymbolMongoModel':
        return cls(**symbol.model_dump(mode='json'))

    @classmethod
    async def to_entity(cls, symbol: dict) -> 'SymbolEntity':
        symbol.pop('id', None)
        return SymbolEntity(**symbol)
