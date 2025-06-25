from injector import Module, provider, singleton, inject
from motor.motor_asyncio import AsyncIOMotorClient
from src.infrastructure.repositories import OrdersRepositoryAdapter, SymbolsRepositoryAdapter


class RepositoriesModule(Module):

    @singleton
    @provider
    @inject
    def provide_orders_repository(self,
                                  client: AsyncIOMotorClient,
                                  database_name: str) -> OrdersRepositoryAdapter:
        return OrdersRepositoryAdapter(client=client, database_name=database_name)

    @singleton
    @provider
    @inject
    def provide_symbols_repository(self,
                                   client: AsyncIOMotorClient,
                                   database_name: str) -> SymbolsRepositoryAdapter:
        return SymbolsRepositoryAdapter(client=client, database_name=database_name)
