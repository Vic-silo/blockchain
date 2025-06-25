from injector import Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import env


class DatabaseModule(Module):

    @singleton
    @provider
    def provide_mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(env.MONGO_URI)

    @singleton
    @provider
    def provide_database_name(self) -> str:
        return env.MONGO_DATABASE
