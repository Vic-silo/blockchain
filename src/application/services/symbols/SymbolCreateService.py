from .SymbolService import SymbolService


class SymbolCreateService(SymbolService):

    async def update_symbols(self):
        # Fetch symbols from third-party
        symbols = await self.symbols_api.fetch_symbols()
        # Store symbols in database
        if symbols:
            await self.repository.store_symbols(symbols=symbols)
