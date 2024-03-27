import uvicorn

from fastapi import FastAPI
from endpoints.routers import api_router
from database.core import core
from config import settings


def get_application():
    application = FastAPI()
    application.include_router(api_router)

    return application

core.create_sa_engine()
core.create_sa_session_factory()

app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
