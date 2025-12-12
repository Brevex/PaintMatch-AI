"""
Gerador de imagens usando Gemini Imagen.

Responsabilidade única: gerar imagens baseadas em descrições textuais.
"""

import uuid

from app.core import ImageGenerationConfig, ImageGenerationError, get_logger, settings

logger = get_logger(__name__)


class GeminiImageGenerator:
    """Implementação de gerador de imagens usando Gemini Imagen."""

    def __init__(self, config: ImageGenerationConfig | None = None) -> None:
        """
        Inicializa o gerador de imagens.

        Args:
            config: Configuração para geração. Usa padrão se não fornecida.
        """
        from google import genai

        self._config = config or ImageGenerationConfig()
        self._client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def generate(self, description: str) -> str:
        """
        Gera uma imagem baseada na descrição.

        Args:
            description: Descrição textual do ambiente/cena

        Returns:
            URL da imagem gerada ou mensagem de erro
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

                    return f"Imagem gerada com sucesso! Você pode visualizá-la aqui: {image_url}"

            return "Não foi possível gerar a imagem."

        except OSError as e:
            logger.exception("File I/O error while saving image: %s", e)
            raise ImageGenerationError(f"Failed to save image: {e}") from e
        except Exception as e:
            logger.exception("Error generating image with Gemini: %s", e)
            return f"Não foi possível gerar a imagem: {e}"

    def _build_prompt(self, description: str) -> str:
        """Constrói o prompt completo para geração."""
        return f"{self._config.prompt_prefix} {description}. {self._config.prompt_suffix}"
