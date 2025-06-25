from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from src.exceptions import SymbolException, RepositoryException
from typing import Any
from src.core import logger
from traceback import format_exc


async def validation_exception_handler(request: Request, exc: Any):
    logger.error(str(format_exc()))
    return JSONResponse(
        status_code=exc.status,
        content={
            "ErrorType": str(type(exc)),
            "ErrorMessage": exc.msg
        }
    )


async def validation_general_exception_handler(request: Request, exc: Exception):
    logger.error(str(format_exc()))
    return JSONResponse(
        status_code=500,
        content={
            "ErrorType": str(type(exc)),
            "ErrorMessage": 'Some error has happened. Review the logs.'
        }
    )


def setup_exception_handlers(app_: FastAPI):
    exceptions = [
        SymbolException, RepositoryException
    ]
    for exc in exceptions:
        app_.add_exception_handler(exc, validation_exception_handler)
    app_.add_exception_handler(Exception, validation_general_exception_handler)
