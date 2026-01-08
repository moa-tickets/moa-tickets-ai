from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.services.loader import load_reviews
from app.services.sentiment import load_model
from app.services.stream import stream_loop

from app.routers.health import router as health_router
from app.routers.reviews import router as reviews_router
from app.routers.keywords import router as keywords_router
from app.routers.predict import router as predict_router
from app.routers.spring_integration import router as spring_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_reviews()
    load_model()
    asyncio.create_task(stream_loop())
    yield
    # shutdown: 필요 시 정리

def create_app() -> FastAPI:
    app = FastAPI(title="Fake Concert Review API", version="0.1.1", lifespan=lifespan)
    app.include_router(health_router)
    app.include_router(reviews_router)
    app.include_router(keywords_router)
    app.include_router(predict_router)
    app.include_router(spring_router)

    return app

app = create_app()
