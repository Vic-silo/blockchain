from ...interfaces import SymbolsRepositoryInterface, BlockchainInterface
from src.domain.entities import SymbolEntity


class SymbolService:

    repository: SymbolsRepositoryInterface
    symbols_api: BlockchainInterface
    entity: SymbolEntity = SymbolEntity

    def __init__(self,
                 repository: SymbolsRepositoryInterface,
                 symbols_api: BlockchainInterface):
        self.repository = repository
        self.symbols_api = symbols_api
