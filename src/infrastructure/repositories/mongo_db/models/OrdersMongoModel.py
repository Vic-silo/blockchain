from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Annotated
from src.domain.entities import OrderEntity

PyObjectId = Annotated[str, BeforeValidator(str)]


class OrderMongoModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias='_id', default=None)
    symbol: str
    order_type: str
    px: float
    qty: float
    value: float

    @classmethod
    async def from_entity(cls, order: OrderEntity) -> 'OrderMongoModel':
        return cls(**order.model_dump(mode='json'))

    async def to_entity(self) -> 'OrderEntity':
        return await OrderEntity.create(symbol=self.symbol,
                                        order_type=self.order_type,
                                        price=self.px, qty=self.qty)
