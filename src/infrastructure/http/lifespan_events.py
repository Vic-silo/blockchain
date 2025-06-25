from fastapi import FastAPI
from src.infrastructure.cli.symbols_controller import update_symbols, \
    update_symbols_async
from contextlib import asynccontextmanager
from src.core import logger
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Load prompts into memory when the app starts.

    Args:
        app (FastAPI): The FastAPI app instance.
    """
    # START UP EVENTS
    logger.info('Starting up the app...')
    await update_symbols_async()

    logger.info('Starting up the app... done')
    # RETURN TO THE APP UNTIL SHUTDOWN
    yield
    # SHUTDOWN EVENTS
    logger.info('Shutting down the app...')
