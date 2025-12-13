"""
Image Generator using Gemini Imagen.

Single responsibility: generate images based on text descriptions.
"""

import uuid

from app.core import ImageGenerationConfig, ImageGenerationError, get_logger, settings

logger = get_logger(__name__)


class GeminiImageGenerator:
    """Implementation of image generator using Gemini Imagen."""

    def __init__(self, config: ImageGenerationConfig | None = None) -> None:
        """
        Initialize the image generator.

        Args:
            config: Generation configuration. Uses default if not provided.
        """
        from google import genai

        self._config = config or ImageGenerationConfig()
        self._client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def generate(self, description: str) -> str:
        """
        Generate an image based on the description.

        Args:
            description: Textual description of the environment/scene.

        Returns:
            URL of the generated image or error message.
        """
        try:
            logger.info("Generating image with description: %s", description)

            prompt = self._build_prompt(description)

            response = self._client.models.generate_content(
                model=self._config.model_name,
                contents=[prompt],
            )

            for part in response.parts:
                if part.text is not None:
                    logger.debug("Response text: %s", part.text)
                elif part.inline_data is not None:
                    image = part.as_image()

                    image_filename = f"{uuid.uuid4()}.png"
                    image_path = settings.images_dir / image_filename

                    image.save(str(image_path))

                    image_url = f"{settings.BASE_URL}/static/images/{image_filename}"
                    logger.info("Image saved at: %s", image_path)
                    logger.info("Image URL: %s", image_url)

                    return f"Image generated successfully! You can view it here: {image_url}"

            return "Could not generate the image."

        except OSError as e:
            logger.exception("File I/O error while saving image: %s", e)
            raise ImageGenerationError(f"Failed to save image: {e}") from e
        except Exception as e:
            logger.exception("Error generating image with Gemini: %s", e)
            return f"Could not generate the image: {e}"

    def _build_prompt(self, description: str) -> str:
        """Build the complete prompt for generation."""
        return f"{self._config.prompt_prefix} {description}. {self._config.prompt_suffix}"
