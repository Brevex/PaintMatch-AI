"""
Unit tests for app/services/ai/image_generator.py

Tests GeminiImageGenerator class following
AAA pattern (Arrange-Act-Assert) and FIRST principles.
"""

from app.core import ImageGenerationConfig
from app.services.ai import GeminiImageGenerator


class TestGeminiImageGeneratorPromptBuilding:
    """Tests for _build_prompt method."""

    def test_build_prompt_concatenates_correctly(self):
        """Test that prompt is correctly built from config and description."""
        # ARRANGE
        config = ImageGenerationConfig(
            prompt_prefix="Uma foto de:",
            prompt_suffix="Sem texto na imagem.",
        )

        class TestableGenerator(GeminiImageGenerator):
            def __init__(self, config):
                self._config = config

        generator = TestableGenerator(config)
        description = "uma casa azul com jardim"

        # ACT
        result = generator._build_prompt(description)

        # ASSERT
        assert result == "Uma foto de: uma casa azul com jardim. Sem texto na imagem."

    def test_build_prompt_with_default_config(self):
        """Test prompt building with default configuration."""
        # ARRANGE
        config = ImageGenerationConfig()

        class TestableGenerator(GeminiImageGenerator):
            def __init__(self, config):
                self._config = config

        generator = TestableGenerator(config)
        description = "casa com tinta vermelha"

        # ACT
        result = generator._build_prompt(description)

        # ASSERT
        assert config.prompt_prefix in result
        assert description in result
        assert config.prompt_suffix in result
