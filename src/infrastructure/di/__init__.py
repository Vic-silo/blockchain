from injector import Injector
from .DataBaseModule import DatabaseModule
from .RepositoryModule import RepositoriesModule
from .ThirdPartyModule import ThirdPartyModule
from .ServicesModule import ServicesModule, OrderCreateService, OrderQueryService, SymbolQueryService, SymbolCreateService


injector: Injector = Injector([
        DatabaseModule(),
        RepositoriesModule(),
        ThirdPartyModule(),
        ServicesModule(),
    ])


def get_order_create_service() -> OrderCreateService:
    return injector.get(OrderCreateService)


def get_order_query_service() -> OrderQueryService:
    return injector.get(OrderQueryService)


def get_symbol_query_service() -> SymbolQueryService:
    return injector.get(SymbolQueryService)


def get_symbol_create_service() -> SymbolCreateService:
    return injector.get(SymbolCreateService)
