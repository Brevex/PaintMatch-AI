"""
Shared fixtures and configuration for unit tests.

These fixtures provide mocked dependencies and test data
following the FIRST principles (Fast, Independent, Repeatable).
"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests")
os.environ.setdefault("GOOGLE_API_KEY", "test-api-key")

import pytest

from app.core.llm_config import (
    AIConfig,
    EmbeddingConfig,
    ImageGenerationConfig,
    LLMConfig,
    RAGConfig,
)
from app.core.ports import ChatResponse, PaintData
from app.schemas.paint import PaintCreate
from app.schemas.user import UserCreate

# =============================================================================
# PaintData Fixtures
# =============================================================================


@pytest.fixture
def sample_paint_data() -> PaintData:
    """Fixture for a complete PaintData object."""
    return PaintData(
        name="Suvinil Toque de Seda",
        color="Branco Neve",
        surface_type="Parede",
        environment="Interno",
        finish_type="Acetinado",
        features="Lavável, antimofo",
        line="Premium",
    )


@pytest.fixture
def paint_data_with_none_values() -> PaintData:
    """Fixture for PaintData with optional fields as None."""
    return PaintData(
        name="Tinta Básica",
        color="Azul",
        surface_type=None,
        environment=None,
        finish_type=None,
        features=None,
        line=None,
    )


@pytest.fixture
def sample_paint_data_list() -> list[PaintData]:
    """Fixture for a list of PaintData objects."""
    return [
        PaintData(
            name="Suvinil Acrílico Fosco",
            color="Verde Selva",
            environment="Externo",
            finish_type="Fosco",
            features="Alta durabilidade",
        ),
        PaintData(
            name="Suvinil Esmalte",
            color="Vermelho Rubi",
            environment="Interno",
            finish_type="Brilhante",
            features="Secagem rápida",
        ),
    ]


# =============================================================================
# Schema Fixtures
# =============================================================================


@pytest.fixture
def sample_user_create() -> UserCreate:
    """Fixture for UserCreate schema."""
    return UserCreate(
        email="test@example.com",
        password="SecurePassword123!",
        full_name="Test User",
    )


@pytest.fixture
def sample_paint_create() -> PaintCreate:
    """Fixture for PaintCreate schema."""
    return PaintCreate(
        name="Suvinil Toque de Seda",
        color="Branco Neve",
        surface_type="Parede",
        environment="Interno",
        finish_type="Acetinado",
        features="Lavável, antimofo",
        line="Premium",
    )


# =============================================================================
# ChatResponse Fixtures
# =============================================================================


@pytest.fixture
def chat_response_with_image() -> ChatResponse:
    """Fixture for ChatResponse with image URL."""
    return ChatResponse(
        answer="Recomendo a tinta Suvinil Acrílico para sua parede externa.",
        image_url="http://localhost:8000/static/images/test-image.png",
    )


@pytest.fixture
def chat_response_without_image() -> ChatResponse:
    """Fixture for ChatResponse without image URL."""
    return ChatResponse(
        answer="Recomendo a tinta Suvinil Acrílico para sua parede externa.",
        image_url=None,
    )


# =============================================================================
# Config Fixtures
# =============================================================================


@pytest.fixture
def default_llm_config() -> LLMConfig:
    """Fixture for default LLM configuration."""
    return LLMConfig()


@pytest.fixture
def custom_llm_config() -> LLMConfig:
    """Fixture for custom LLM configuration."""
    return LLMConfig(model_name="gemini-pro", temperature=0.5)


@pytest.fixture
def default_rag_config() -> RAGConfig:
    """Fixture for default RAG configuration."""
    return RAGConfig.default()


@pytest.fixture
def default_ai_config() -> AIConfig:
    """Fixture for default AI configuration."""
    return AIConfig.default()


@pytest.fixture
def default_embedding_config() -> EmbeddingConfig:
    """Fixture for default embedding configuration."""
    return EmbeddingConfig()


@pytest.fixture
def default_image_generation_config() -> ImageGenerationConfig:
    """Fixture for default image generation configuration."""
    return ImageGenerationConfig()
