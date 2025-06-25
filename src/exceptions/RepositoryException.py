__all__ = [
    "RepositoryException",
    "UnknownTableException",
    "QueryException",
    "NotElementsFoundException"
]

class RepositoryException(Exception):
    pass


class UnknownTableException(RepositoryException):
    """
    Exception raised while getting table/collection
    """
    msg: str = 'Unknown table for the repository adapter.'
    status: int = 500


class QueryException(RepositoryException):
    """
    Exception raised while executing query
    """
    msg: str = 'An error occurs while executing a query.'
    status: int = 500


class NotElementsFoundException(RepositoryException):
    """
    Exception raised while executing query
    """
    msg: str = 'Not exist registers for the given filters.'
    status: int = 404
