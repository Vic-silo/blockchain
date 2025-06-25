from enum import Enum

__all__ = [
    'Defaults',
    'OrderType'
]


class Defaults(Enum):

    STR = 'N/A'
    DEC = -1
    FLOAT = -1.1


class OrderType(Enum):

    BUY = 'bid'
    SELL = 'ask'
