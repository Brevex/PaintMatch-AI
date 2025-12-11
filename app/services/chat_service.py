"""
Serviço de Chat - Fachada Principal.

Orquestra os componentes de IA para fornecer respostas contextuais
sobre tintas e gerar visualizações quando solicitado.
"""

import re

from app.core.llm_config import DEFAULT_AI_CONFIG, AIConfig
from app.core.ports import ChatResponse
from app.services.ai.agent_builder import AgentBuilder
from app.services.ai.image_generator import GeminiImageGenerator
from app.services.ai.paint_repository import SqlAlchemyPaintRepository
from app.services.ai.rag_builder import RAGChainBuilder

_URL_PATTERN = re.compile(r"https?://[^\s)]+")


class ChatService:
    """
    Serviço principal de chat com IA.

    Atua como fachada, delegando responsabilidades específicas
    para componentes especializados.
    """

    def __init__(
        self,
        config: AIConfig | None = None,
        paint_repository: SqlAlchemyPaintRepository | None = None,
        image_generator: GeminiImageGenerator | None = None,
    ) -> None:
        """Inicializa o serviço de chat."""
        print("Iniciando o ChatService com Agente Gemini...")

        self._config = config or DEFAULT_AI_CONFIG
        self._paint_repository = paint_repository or SqlAlchemyPaintRepository()
        self._image_generator = image_generator or GeminiImageGenerator(
            self._config.image_generation
        )

        self._agent_executor = None

        print("ChatService inicializado (Agente será carregado sob demanda).")

    @property
    def agent_executor(self):
        """Acesso lazy ao executor do agente."""
        if self._agent_executor is None:
            self._agent_executor = self._build_agent()
        return self._agent_executor

    def _build_agent(self):
        """Constrói o agente usando os componentes modulares."""
        paints = self._paint_repository.get_all_paints()

        if not paints:
            print("Aviso: Nenhuma tinta disponível no banco de dados.")
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
        """Processa uma consulta e retorna a resposta do assistente."""
        if not self.agent_executor:
            self._agent_executor = self._build_agent()
            if not self.agent_executor:
                return ChatResponse(
                    answer=(
                        "O sistema de IA está inicializando ou o banco de dados "
                        "de tintas está vazio. Por favor, tente novamente mais "
                        "tarde ou contate o administrador."
                    )
                ).to_dict()

        try:
            response = self.agent_executor.invoke({"input": query})
            output_text = response.get("output", "Não consegui processar sua solicitação.")

            image_url = self._extract_url(output_text)

            return ChatResponse(answer=output_text, image_url=image_url).to_dict()

        except Exception as e:
            print(f"Erro ao invocar o agente: {e}")
            return ChatResponse(answer="Ocorreu um erro ao processar sua solicitação.").to_dict()

    def _extract_url(self, text: str) -> str | None:
        """Extrai URL de uma resposta, se presente."""
        match = _URL_PATTERN.search(text)
        return match.group(0) if match else None


def create_chat_service(config: AIConfig | None = None) -> ChatService:
    """Factory function para criar instâncias de ChatService."""
    return ChatService(config=config)
