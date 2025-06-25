from injector import Module, provider, singleton
from src.infrastructure.third_party import BlockchainAPI


class ThirdPartyModule(Module):

    @singleton
    @provider
    def provide_blockchain_api(self) -> BlockchainAPI:
        return BlockchainAPI()
