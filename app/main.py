"""Main entry point for the FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import auth, chat, paints, users
from app.core import get_logger
from app.core.config import settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler for application startup and shutdown.

    Pre-warms the chat agent on startup to avoid latency
    on the first user request.
    """
    logger.info("Starting application lifespan...")

    try:
        from app.api.v1.deps import get_chat_service

        service = get_chat_service()
        _ = service.agent_executor
        logger.info("ChatService agent pre-warmed successfully")
    except Exception as e:
        logger.warning("Failed to pre-warm ChatService agent: %s", e)

    yield

    logger.info("Application shutdown complete")


app = FastAPI(
    title="Intelligent Paint Catalog with AI",
    description="API for a virtual assistant expert in Suvinil paints.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(paints.router, prefix="/api/v1/paints", tags=["Paints"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])


@app.get("/")
def read_root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to the Intelligent Paint Catalog!"}
