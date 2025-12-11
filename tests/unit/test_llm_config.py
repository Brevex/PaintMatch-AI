"""
Unit tests for app/core/llm_config.py

Tests configuration dataclasses and their validation following
AAA pattern (Arrange-Act-Assert) and FIRST principles.
"""

import pytest

from app.core import (
    AIConfig,
    EmbeddingConfig,
    ImageGenerationConfig,
    LLMConfig,
    RAGConfig,
)


class TestLLMConfig:
    """Tests for LLMConfig dataclass."""

    def test_llm_config_valid_temperature(self):
        """Test that valid temperature values are accepted."""
        # ARRANGE & ACT
        config = LLMConfig(temperature=0.5)

        # ASSERT
        assert config.temperature == 0.5
        assert config.model_name == "gemini-2.5-flash-lite"

    def test_llm_config_boundary_temperature_zero(self):
        """Edge case: temperature at lower boundary (0.0) is valid."""
        # ARRANGE & ACT
        config = LLMConfig(temperature=0.0)

        # ASSERT
        assert config.temperature == 0.0

    def test_llm_config_boundary_temperature_max(self):
        """Edge case: temperature at upper boundary (2.0) is valid."""
        # ARRANGE & ACT
        config = LLMConfig(temperature=2.0)

        # ASSERT
        assert config.temperature == 2.0

    def test_llm_config_invalid_temperature_raises(self):
        """Failure case: temperature outside valid range raises ValueError."""
        # ARRANGE & ACT & ASSERT
        with pytest.raises(ValueError, match="temperature deve estar entre 0.0 e 2.0"):
            LLMConfig(temperature=2.5)

    def test_llm_config_negative_temperature_raises(self):
        """Failure case: negative temperature raises ValueError."""
        # ARRANGE & ACT & ASSERT
        with pytest.raises(ValueError, match="temperature deve estar entre 0.0 e 2.0"):
            LLMConfig(temperature=-0.1)


class TestEmbeddingConfig:
    """Tests for EmbeddingConfig dataclass."""

    def test_embedding_config_default_model(self):
        """Test default embedding model name."""
        # ARRANGE & ACT
        config = EmbeddingConfig()

        # ASSERT
        assert config.model_name == "models/embedding-001"


class TestImageGenerationConfig:
    """Tests for ImageGenerationConfig dataclass."""

    def test_image_generation_config_defaults(self):
        """Test default image generation configuration."""
        # ARRANGE & ACT
        config = ImageGenerationConfig()

        # ASSERT
        assert config.model_name == "gemini-2.5-flash-image"
        assert config.number_of_images == 1
        assert "foto realista" in config.prompt_prefix


class TestRAGConfig:
    """Tests for RAGConfig dataclass."""

    def test_rag_config_default_creation(self):
        """Test that RAGConfig.default() creates valid configuration."""
        # ARRANGE & ACT
        config = RAGConfig.default()

        # ASSERT
        assert isinstance(config.llm, LLMConfig)
        assert isinstance(config.embedding, EmbeddingConfig)


class TestAIConfig:
    """Tests for AIConfig dataclass."""

    def test_ai_config_default_creation(self):
        """Test that AIConfig.default() creates all necessary configs."""
        # ARRANGE & ACT
        config = AIConfig.default()

        # ASSERT
        assert isinstance(config.rag, RAGConfig)
        assert isinstance(config.image_generation, ImageGenerationConfig)
        assert isinstance(config.agent_llm, LLMConfig)

    def test_ai_config_immutability(self):
        """Test that AIConfig is frozen (immutable)."""
        # ARRANGE
        config = AIConfig.default()

        # ACT & ASSERT
        with pytest.raises(AttributeError):
            config.agent_llm = LLMConfig(temperature=1.0)
