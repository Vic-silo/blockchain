from injector import Module, provider, singleton, inject
from src.application.services import (OrderCreateService, OrderQueryService,
                                      SymbolCreateService, SymbolQueryService)
from src.infrastructure.repositories import OrdersRepositoryAdapter, SymbolsRepositoryAdapter
from src.infrastructure.third_party import BlockchainAPI


class ServicesModule(Module):

    @singleton
    @provider
    @inject
    def provide_order_create_service(self, orders_repo: OrdersRepositoryAdapter,
                                     blockchain_api: BlockchainAPI) -> OrderCreateService:
        return OrderCreateService(repository=orders_repo, order_api=blockchain_api)

    @singleton
    @provider
    @inject
    def provide_order_query_service(self, orders_repo: OrdersRepositoryAdapter,
                                    blockchain_api: BlockchainAPI) -> OrderQueryService:
        return OrderQueryService(repository=orders_repo, order_api=blockchain_api)

    @singleton
    @provider
    @inject
    def provide_symbol_create_service(self, symbols_repo: SymbolsRepositoryAdapter,
                                      blockchain_api: BlockchainAPI) -> SymbolCreateService:
        return SymbolCreateService(repository=symbols_repo, symbols_api=blockchain_api)

    @singleton
    @provider
    @inject
    def provide_symbol_query_service(self, symbols_repo: SymbolsRepositoryAdapter,
                                     blockchain_api: BlockchainAPI) -> SymbolQueryService:
        return SymbolQueryService(repository=symbols_repo, symbols_api=blockchain_api)
