"""
Chat Service - Main Facade.

Orchestrates AI components to provide contextual answers
about paints and generate visualizations when requested.
"""

import re

from app.core import (
    DEFAULT_AI_CONFIG,
    AIConfig,
    AIServiceError,
    ImageGenerator,
    PaintRepository,
    get_logger,
)
from app.schemas.chat import ChatResponse
from app.services.ai import (
    AgentBuilder,
    GeminiImageGenerator,
    RAGChainBuilder,
    SqlAlchemyPaintRepository,
)

_URL_PATTERN = re.compile(r"https?://[^\s)]+")
logger = get_logger(__name__)


class ChatService:
    """
    Main AI chat service.

    Acts as a facade, delegating specific responsibilities
    to specialized components.
    """

    def __init__(
        self,
        config: AIConfig | None = None,
        paint_repository: PaintRepository | None = None,
        image_generator: ImageGenerator | None = None,
    ) -> None:
        """Initialize the chat service."""
        logger.info("Initializing ChatService with Gemini Agent...")

        self._config = config or DEFAULT_AI_CONFIG
        self._paint_repository: PaintRepository = paint_repository or SqlAlchemyPaintRepository()
        self._image_generator: ImageGenerator = image_generator or GeminiImageGenerator(
            self._config.image_generation
        )

        self._agent_executor = None

        logger.info("ChatService initialized (Agent will be loaded on demand)")

    @property
    def agent_executor(self):
        """Lazy access to the agent executor."""
        if self._agent_executor is None:
            self._agent_executor = self._build_agent()
        return self._agent_executor

    def _build_agent(self):
        """Build the agent using modular components."""
        paints = self._paint_repository.get_all_paints()

        if not paints:
            logger.warning("No paints available in database")
            return None

        rag_builder = RAGChainBuilder(self._config.rag)
        rag_chain = rag_builder.build(paints)

        if rag_chain is None:
            return None

        agent_builder = AgentBuilder(self._config.agent_llm)
        return agent_builder.build(
            rag_chain_invoke=rag_chain.invoke, image_generator_func=self._image_generator.generate
        )

    def get_ai_response(self, query: str) -> dict:
        """Process a query and return the assistant's response."""
        if not self.agent_executor:
            self._agent_executor = self._build_agent()
            if not self.agent_executor:
                return ChatResponse(
                    answer=(
                        "The AI system is initializing or the paint database "
                        "is empty. Please try again later "
                        "or contact the administrator."
                    )
                ).to_dict()

        try:
            response = self.agent_executor.invoke({"input": query})
            output_text = response.get("output", "I could not process your request.")

            image_url = self._extract_url(output_text)

            return ChatResponse(answer=output_text, image_url=image_url).to_dict()

        except AIServiceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            logger.exception("Data processing error: %s", e)
            return ChatResponse(answer="Error processing response data.").to_dict()
        except Exception as e:
            logger.exception("Unexpected error invoking agent: %s", e)
            return ChatResponse(answer="An error occurred while processing your request.").to_dict()

    @staticmethod
    def _extract_url(text: str) -> str | None:
        """Extract URL from response, if present."""
        match = _URL_PATTERN.search(text)
        return match.group(0) if match else None


def create_chat_service(config: AIConfig | None = None) -> ChatService:
    """Factory function to create ChatService instances."""
    return ChatService(config=config)
