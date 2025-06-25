from typer import Typer
from .orders_controller import app_cli as app_orders
from .symbols_controller import app_cli as app_symbols
from src.exceptions import SymbolException, RepositoryException
from . import logger_cli

app_cli = Typer()
app_cli.add_typer(app_orders, name='orders')
app_cli.add_typer(app_symbols, name='symbols')


if __name__ == '__main__':
    try:
        app_cli()

    except (SymbolException, RepositoryException) as e:
        logger_cli.error(f'Error: {e.msg}')
