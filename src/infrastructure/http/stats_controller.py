from src.infrastructure.di import get_order_create_service, get_symbol_query_service, get_order_query_service
from fastapi import APIRouter, Depends
from src.application.services.orders import OrderQueryService
from src.application.services.symbols import SymbolQueryService

router = APIRouter(prefix='/stats')


@router.get("/orders")
async def fetch_symbol_stats_by_order_type(
        symbol: str,
        order_type: str,
        service: SymbolQueryService = Depends(get_symbol_query_service),
        order_service: OrderQueryService = Depends(get_order_query_service)):

    return await service.fetch_symbol_stats_by_order_type(
        symbol=symbol, order_type=order_type, order_service=order_service)


@router.get("/whole")
async def fetch_whole_stats(
        service: SymbolQueryService = Depends(get_symbol_query_service),
        order_service: OrderQueryService = Depends(get_order_query_service)):
    return await service.fetch_symbol_stats_whole(order_service=order_service)
