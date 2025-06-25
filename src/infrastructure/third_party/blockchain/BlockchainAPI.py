from src.core.config import env
from src.application.interfaces import BlockchainInterface
from .models import SymbolStatus, OrderBook
from src.domain.entities import SymbolEntity, OrderEntity
from typing import List
from src.infrastructure.third_party import APIBase
from src.core import logger
from httpx import HTTPStatusError


class BlockchainAPI(BlockchainInterface, APIBase):

    API_KEY: str = env.BLOCKCHAIN_API_KEY
    BASE_URL: str = env.BLOCKCHAIN_BASE_URL

    def __init__(self):
        logger.debug('Instantiating BlockchainAPI...')
        APIBase.__init__(self, timeout=30)

    @property
    def headers(self) -> dict:
        return {'Accept': 'application/json', 'X-API-Token': self.API_KEY}

    async def fetch_symbols(self) -> List[SymbolEntity]:
        """
        Get all the SymbolStatus information
        :return:
        """
        url = f'{self.BASE_URL}/symbols'
        response = await self.client.get(url=url, headers=self.headers)
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            logger.warn('[!] The symbols could not be loaded. Will be used the'
                        ' currently stored if them exist.')
            logger.warn(e.__str__())
            return []

        return await SymbolStatus.to_entity_whole(response=response.json())

    async def fetch_order_book_l3(self,
                                  compound_symbol: str) -> List[OrderEntity]:
        """Level 3 Order Book data is available through the l3 channel.
        Each entry in bids and asks arrays is an order, along with its id (id),
        price (px) and quantity (qty) attributes.
        :param compound_symbol: Crypto-Currency keys
        :return:
        """
        url = f'{self.BASE_URL}/l3/{compound_symbol}'
        response = await self.client.get(url=url, headers=self.headers)
        response.raise_for_status()

        return await OrderBook(**response.json()).to_entity()
