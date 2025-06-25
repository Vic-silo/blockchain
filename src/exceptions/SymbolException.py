__all__ = [
    "SymbolException",
    "SymbolStatusParseException",
    "UnknownSymbolException",
    "EmptySymbolException"
]

class SymbolException(Exception):
    pass


class SymbolStatusParseException(SymbolException):
    """
    Exception raised while parsing SymbolStatus
    """
    msg: str = 'Fetch and parse SymbolStatus has failed.'
    status: int = 500


class UnknownSymbolException(SymbolException):
    """
    Exception raised while parsing SymbolStatus
    """
    msg: str = 'Fetch and parse SymbolStatus has failed.'
    status: int = 500


class EmptySymbolException(SymbolException):
    """
    Exception raised when not exist symbols in database
    """
    msg: str = 'Not exist symbols registers in database.'
    status: int = 500
