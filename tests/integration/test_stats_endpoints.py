import pytest
from unittest.mock import patch, AsyncMock
from src.infrastructure.di import get_symbol_query_service, \
    get_order_query_service
from src.infrastructure.http.main_controller import app
from src.application.services import OrderQueryService, SymbolQueryService


class TestStatsEndpoints:

    @pytest.mark.asyncio
    async def test_fetch_whole_stats_success(
            self,
            client,
            mock_orders_repository,
            mock_symbols_repository,
            mock_blockchain_api,
            sample_orders_entity_list_two_symbols,
            sample_symbols_entity_list
    ):
        """Test the /stats/whole endpoint with mocked services."""
        # Arrange
        expected_stats = {
            "BTC-USD": {
                "bids": {"count": 2, "qty": 0.2, "value": 10000.0},
                "asks": {"count": 2, "qty": 0.2, "value": 10000.0}
            },
            "BTC-EUR": {
                "bids": {"count": 2, "qty": 0.2, "value": 10000.0},
                "asks": {"count": 2, "qty": 0.2, "value": 10000.0}
            }
        }
        # Mock repositories
        mock_orders_repository.fetch_orders.side_effect = [
            sample_orders_entity_list_two_symbols,  # first call for symbol
            [],  # second call for symbol. Avoid duplicate mocked response
        ]
        mock_symbols_repository.fetch_symbols.return_value = sample_symbols_entity_list
        # Instance services for integration
        order_service = OrderQueryService(repository=mock_orders_repository,
                                          order_api=mock_blockchain_api)
        symbol_service = SymbolQueryService(repository=mock_symbols_repository,
                                            symbols_api=mock_blockchain_api)
        # Override app dependencies
        app.dependency_overrides[
            get_symbol_query_service] = lambda: symbol_service
        app.dependency_overrides[
            get_order_query_service] = lambda: order_service

        # Act
        response = client.get("/stats/whole")
        # Assert
        assert response.status_code == 200
        assert response.json() == expected_stats
        app.dependency_overrides = {}
