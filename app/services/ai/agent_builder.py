"""
Orchestrator Agent Builder.

Single responsibility: Build and configure the agent
that orchestrates the recommendation and image generation tools.
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
    """Orchestrator agent builder."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        """
        Initialize the builder.

        Args:
            config: Agent LLM configuration. Uses default if not provided.
        """
        self._config = config or LLMConfig()

    def build(
        self,
        rag_chain_invoke: Callable[[str], str],
        image_generator_func: Callable[[str], str],
    ) -> AgentExecutor | None:
        """
        Build the orchestrator agent with tools.

        Args:
            rag_chain_invoke: Function to invoke the RAG chain.
            image_generator_func: Function to generate images.

        Returns:
            Configured AgentExecutor, or None if not possible.
        """
        if rag_chain_invoke is None:
            logger.warning("RAG chain not available. Agent cannot be built.")
            return None

        tools = self._create_tools(rag_chain_invoke, image_generator_func)

        from langchain_classic.agents import AgentExecutor, create_react_agent
        from langchain_core.prompts import PromptTemplate

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
        """Create the list of tools for the agent."""
        from langchain_core.tools import Tool

        return [
            Tool(
                name="PaintRecommender",
                func=rag_chain_invoke,
                description=PROMPTS.PAINT_RECOMMENDER_DESCRIPTION,
            ),
            Tool(
                name="RoomImageGenerator",
                func=image_generator_func,
                description=PROMPTS.IMAGE_GENERATOR_DESCRIPTION,
            ),
        ]

    def _create_llm(self) -> ChatGoogleGenerativeAI:
        """Create the agent LLM instance."""
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=self._config.model_name,
            temperature=self._config.temperature,
            google_api_key=settings.GOOGLE_API_KEY,
        )
