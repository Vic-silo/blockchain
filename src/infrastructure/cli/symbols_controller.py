import typer
from typer import Typer
from src.infrastructure.di import injector
from src.application.services import SymbolCreateService
from . import logger_cli
from traceback import format_exc
from asyncio import run

app_cli = Typer()

symbol_create_service: SymbolCreateService = injector.get(SymbolCreateService)


@app_cli.command()
def update_symbols() -> None:
    """
    Fetch symbols from third party and load them into database
    :return:
    """
    try:
        run(symbol_create_service.update_symbols())

    except Exception as e:
        logger_cli.error(f'Error during updating symbols:\n{format_exc()}')
        raise e

    else:
        success_msg = '[+] SUCCESS: symbols extracted and loaded in database'
        typer.echo(success_msg)
        logger_cli.info(success_msg)


async def update_symbols_async() -> None:
    """
    Fetch symbols from third party and load them into database
    :return:
    """
    try:
        await symbol_create_service.update_symbols()

    except Exception as e:
        logger_cli.error(f'Error during updating symbols:\n{format_exc()}')
        raise e

    else:
        success_msg = '[+] SUCCESS: symbols extracted and loaded in database'
        logger_cli.info(success_msg)
