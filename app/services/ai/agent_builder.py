"""
Construtor do Agente Orquestrador.

Responsabilidade única: construir e configurar o agente
que orquestra as ferramentas de recomendação e geração de imagens.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_classic.agents import AgentExecutor
    from langchain_core.tools import Tool
    from langchain_google_genai import ChatGoogleGenerativeAI

from app.core import PROMPTS, LLMConfig, get_logger, settings

logger = get_logger(__name__)


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
        rag_chain_invoke: Callable[[str], str],
        image_generator_func: Callable[[str], str],
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
            logger.warning("RAG chain not available. Agent cannot be built.")
            return None

        tools = self._create_tools(rag_chain_invoke, image_generator_func)

        from langchain_classic.agents import AgentExecutor, create_react_agent
        from langchain_core.prompts import PromptTemplate

        # Prompt ReAct padrão (hwchase17/react)
        react_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(react_template)
        llm = self._create_llm()

        agent = create_react_agent(llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    def _create_tools(
        self,
        rag_chain_invoke: Callable[[str], str],
        image_generator_func: Callable[[str], str],
    ) -> list[Tool]:
        """Cria a lista de ferramentas do agente."""
        from langchain_core.tools import Tool

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
