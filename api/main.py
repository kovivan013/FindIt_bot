import uvicorn

from fastapi import FastAPI
from network.routers import api_router
from services.errors_reporter import Reporter
from database.core import core
from config import settings


def get_application():
    application = FastAPI()
    application.include_router(api_router)

    return application

core.create_sa_engine()
core.create_sa_session_factory()

app = get_application()

Reporter.start(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
