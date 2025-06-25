from fastapi import FastAPI
from .stats_controller import router as stats_router
from .exceptions_controller import setup_exception_handlers
from .lifespan_events import lifespan
import uvicorn


__version__ = '/api/v1'

app = FastAPI(title="t2ó - Technical test", version=__version__)

# Include routers
app.include_router(stats_router, tags=['stats'])
# Include events
app.router.lifespan_context = lifespan

# Setup exceptions handlers
setup_exception_handlers(app_=app)


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
