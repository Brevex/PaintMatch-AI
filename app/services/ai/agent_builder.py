"""
Construtor do Agente Orquestrador.

Responsabilidade única: construir e configurar o agente
que orquestra as ferramentas de recomendação e geração de imagens.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain.agents import AgentExecutor
    from langchain.tools import Tool
    from langchain_google_genai import ChatGoogleGenerativeAI

from app.core import PROMPTS, LLMConfig, settings


class AgentBuilder:
    """Construtor do agente orquestrador."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        """
        Inicializa o construtor.

        Args:
            config: Configuração do LLM do agente. Usa padrão se não fornecida.
        """
        self._config = config or LLMConfig()

    def build(
        self,
        rag_chain_invoke: callable,
        image_generator_func: callable,
    ) -> AgentExecutor | None:
        """
        Constrói o agente orquestrador com as ferramentas.

        Args:
            rag_chain_invoke: Função para invocar a RAG chain
            image_generator_func: Função para gerar imagens

        Returns:
            AgentExecutor configurado, ou None se não for possível
        """
        if rag_chain_invoke is None:
            print("Aviso: RAG chain não disponível. Agente não pode ser construído.")
            return None

        tools = self._create_tools(rag_chain_invoke, image_generator_func)

        from langchain import hub
        from langchain.agents import AgentExecutor, create_react_agent

        prompt = hub.pull("hwchase17/react")
        llm = self._create_llm()

        agent = create_react_agent(llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    def _create_tools(
        self,
        rag_chain_invoke: callable,
        image_generator_func: callable,
    ) -> list[Tool]:
        """Cria a lista de ferramentas do agente."""
        from langchain.tools import Tool

        return [
            Tool(
                name="RecomendadorDeTintas",
                func=rag_chain_invoke,
                description=PROMPTS.PAINT_RECOMMENDER_DESCRIPTION,
            ),
            Tool(
                name="GeradorDeImagemDeAmbiente",
                func=image_generator_func,
                description=PROMPTS.IMAGE_GENERATOR_DESCRIPTION,
            ),
        ]

    def _create_llm(self) -> ChatGoogleGenerativeAI:
        """Cria a instância do LLM do agente."""
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=self._config.model_name,
            temperature=self._config.temperature,
            google_api_key=settings.GOOGLE_API_KEY,
        )
