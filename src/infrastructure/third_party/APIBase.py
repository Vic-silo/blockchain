from src.core import logger
from httpx import Request, Response, AsyncClient


class APIBase:

    def __init__(self, **client_kwargs):
        logger.debug('Instantiating APIBase...')
        self.client = AsyncClient(
            event_hooks={
                "request": [self.log_request],
                "response": [self.log_response],
            },
            **client_kwargs
        )

    @property
    def client(self):
        if not self._client:
            raise AttributeError('self._client for APIBase is not created.')
        logger.debug(f'getting {self._client=}')
        return self._client

    @client.setter
    def client(self, value: AsyncClient):
        self._client = value

    @staticmethod
    async def log_request(request: Request):
        logger.info(f"Request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")
        if request.content:
            logger.debug(f"Body: {request.content.decode()}")

    @staticmethod
    async def log_response(response: Response):
        logger.info(f"Response: {response.status_code} {response.url}")
        logger.debug(f"Headers: {response.headers}")
        content = await response.aread()
        logger.debug(f"Body: {content.decode(errors='replace')}")
