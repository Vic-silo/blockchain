from ...interfaces import BlockchainInterface, OrdersRepositoryInterface


class OrderService:

    repository: OrdersRepositoryInterface
    order_api: BlockchainInterface

    def __init__(self,
                 repository: OrdersRepositoryInterface,
                 order_api: BlockchainInterface):
        self.repository = repository
        self.order_api = order_api
