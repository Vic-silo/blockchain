import pytest
import asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from src.infrastructure.http.main_controller import app
from src.infrastructure.repositories import OrdersRepositoryAdapter, SymbolsRepositoryAdapter
from src.infrastructure.third_party import BlockchainAPI
from src.domain.entities import SymbolEntity, OrderEntity


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_mongo_client():
    """Mock MongoDB client."""
    return AsyncMock(spec=AsyncIOMotorClient)


@pytest.fixture
def mock_blockchain_api():
    """Mock BlockchainAPI."""
    mock_api = AsyncMock(spec=BlockchainAPI)
    mock_api.fetch_symbols = AsyncMock()
    mock_api.fetch_order_book_l3 = AsyncMock()
    return mock_api


@pytest.fixture
def mock_orders_repository(mock_mongo_client):
    """Mock OrdersRepositoryAdapter."""
    repo = OrdersRepositoryAdapter(client=mock_mongo_client, database_name="test_db")
    repo.store_orders = AsyncMock()
    repo.fetch_orders = AsyncMock()
    return repo


@pytest.fixture
def mock_symbols_repository(mock_mongo_client):
    """Mock SymbolsRepositoryAdapter."""
    repo = SymbolsRepositoryAdapter(client=mock_mongo_client, database_name="test_db")
    repo.store_symbols = AsyncMock()
    repo.fetch_symbols = AsyncMock()
    return repo


@pytest.fixture
def sample_symbol_entity():
    """Sample SymbolEntity for testing."""
    return SymbolEntity(
        id_symbol=1,
        compound_symbol="BTC-USD",
        base_currency="BTC-USD",
        base_currency_scale=8,
        counter_currency="BTC-USD",
        counter_currency_scale=2,
        status="open",
    )


@pytest.fixture
def sample_order_entity():
    """Sample OrderEntity for testing."""
    return asyncio.run(OrderEntity.create(
        symbol="BTC-USD",
        order_type="bid",
        price = 50000.0,
        qty = 0.1
    ))


@pytest.fixture
def sample_symbols_entity_list(sample_symbol_entity):
    """List of sample symbols."""
    return [
        sample_symbol_entity,
        SymbolEntity(
            id_symbol=2,
            compound_symbol="BTC-EUR",
            base_currency="BTC-EUR",
            base_currency_scale=8,
            counter_currency="BTC-EUR",
            counter_currency_scale=2,
            status="open",
        )
    ]


@pytest.fixture
def sample_orders_entity_list(sample_order_entity):
    """List of sample orders."""
    order2 = asyncio.run(OrderEntity.create(
        symbol="BTC-USD",
        order_type="ask",
        price=50000.0,
        qty=0.1
    ))
    return [
        sample_order_entity,
        order2
    ]


@pytest.fixture
def sample_orders_entity_list_two_symbols():
    """List of sample orders."""
    order1 = asyncio.run(OrderEntity.create(
        symbol="BTC-USD",
        order_type="bid",
        price=50000.0,
        qty=0.1
    ))
    order2 = asyncio.run(OrderEntity.create(
        symbol="BTC-EUR",
        order_type="ask",
        price=50000.0,
        qty=0.1
    ))
    order3 = asyncio.run(OrderEntity.create(
        symbol="BTC-EUR",
        order_type="bid",
        price=50000.0,
        qty=0.1
    ))
    order4 = asyncio.run(OrderEntity.create(
        symbol="BTC-USD",
        order_type="ask",
        price=50000.0,
        qty=0.1
    ))
    return [order1, order1, order2, order2, order3, order3, order4, order4]
