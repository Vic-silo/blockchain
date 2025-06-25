import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.infrastructure.third_party import BlockchainAPI
from src.infrastructure.third_party.blockchain.models import SymbolStatus


class TestBlockchainAPI:

    def setup_method(self):
        """Setup test dependencies."""
        self.api = BlockchainAPI()
        self.api.client = AsyncMock()

    @pytest.mark.asyncio
    async def test_fetch_symbols(self, sample_symbols_entity_list):
        """Test successful symbols fetch from API."""
        # Arrange
        # Mock request
        mock_response = MagicMock()
        mock_response.json.return_value = {
                "BTC-USD": {"base_currency": "BTC-USD","base_currency_scale": 8,"counter_currency": "BTC-USD","counter_currency_scale": 2,"min_price_increment": 10,"min_price_increment_scale": 0,"min_order_size": 10,"min_order_size_scale": 2,"max_order_size": 0,"max_order_size_scale": 8,"lot_size": 5,"lot_size_scale": 2,"status": "open","id": 1,"auction_price": 0,"auction_size": 0,"auction_time": "1530","imbalance": 0},
                "BTC-EUR": {"base_currency": "BTC-EUR","base_currency_scale": 8,"counter_currency": "BTC-EUR","counter_currency_scale": 2,"min_price_increment": 10,"min_price_increment_scale": 0,"min_order_size": 10,"min_order_size_scale": 2,"max_order_size": 0,"max_order_size_scale": 8,"lot_size": 5,"lot_size_scale": 2,"status": "open","id": 2,"auction_price": 0,"auction_size": 0,"auction_time": "1530","imbalance": 0}
            }
        mock_response.raise_for_status.return_value = None
        self.api.client.get.return_value = mock_response

        # Mock SymbolStatus.to_entity_whole method
        with patch.object(SymbolStatus,
                          attribute='to_entity_whole',
                          new_callable=AsyncMock) as mock_to_entity:
            mock_to_entity.return_value = sample_symbols_entity_list

            # Act
            result = await self.api.fetch_symbols()

            # Assert
            assert result == sample_symbols_entity_list
            self.api.client.get.assert_called_once()
            mock_to_entity.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_fetch_order_book_l3(self, sample_orders_entity_list):
        """Test successful order book fetch from API."""
        # Arrange
        # Mock request
        compound_symbol = "BTC-USD"
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "symbol": compound_symbol,
            "bids": [{"num": "1", "px": 50000.0, "qty": 0.1}],
            "asks": [{"num": "2", "px": 50000.0, "qty": 0.1}]
        }
        mock_response.raise_for_status.return_value = None
        self.api.client.get.return_value = mock_response

        # Mock OrderBook.to_entity method
        with patch('src.infrastructure.third_party.blockchain.models.OrderBook') as mock_orderbook_class:
            mock_orderbook_instance = MagicMock()
            mock_orderbook_instance.to_entity = AsyncMock(return_value=sample_orders_entity_list)
            mock_orderbook_class.return_value = mock_orderbook_instance

            # Act
            result = await self.api.fetch_order_book_l3(compound_symbol)

            # Assert
            assert result == sample_orders_entity_list
            self.api.client.get.assert_called_once()

    def test_headers_property(self):
        """Test headers property returns correct format."""
        # Act
        headers = self.api.headers

        # Assert
        assert "Accept" in headers
        assert "X-API-Token" in headers
        assert headers["Accept"] == "application/json"
