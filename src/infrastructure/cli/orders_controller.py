import typer
from typer import Typer
from src.infrastructure.di import injector
from src.application.services import OrderCreateService, SymbolQueryService
from . import logger_cli
from traceback import format_exc
from asyncio import run, gather

app_cli = Typer()

order_create_service: OrderCreateService = injector.get(OrderCreateService)
symbol_query_service: SymbolQueryService = injector.get(SymbolQueryService)


@app_cli.command()
def load_l3_orders(symbol: str = None) -> None:
    try:
        run(load_l3_orders_process(symbol=symbol))

    except Exception as e:
        logger_cli.error(f'Error during getting l3 orders:\n{format_exc()}')
        raise e

    else:
        success_msg = '[+] SUCCESS: l3 orders extracted and loaded in database'
        typer.echo(success_msg)
        logger_cli.info(success_msg)


async def load_l3_orders_process(symbol: str = None):
    """
    Process the given symbol or all the available symbols
    :param symbol:
    :return:
    """
    symbols = [symbol]
    if not symbol:
        symbols = await symbol_query_service.fetch_symbols()
    tasks = [order_create_service.store_order(
        symbol=symbol, symbol_service=symbol_query_service)
        for symbol in symbols]
    await gather(*tasks)
