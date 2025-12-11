"""
Configurações tipadas para componentes de IA.

Este módulo centraliza todas as configurações relacionadas aos modelos
de linguagem, embeddings e geração de imagens, seguindo o princípio
de configuração explícita e imutável.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    """Configuração para modelos de linguagem (LLM)."""

    model_name: str = "gemini-2.5-flash-lite"
    temperature: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("temperature deve estar entre 0.0 e 2.0")


@dataclass(frozen=True)
class EmbeddingConfig:
    """Configuração para modelos de embedding."""

    model_name: str = "models/embedding-001"


@dataclass(frozen=True)
class ImageGenerationConfig:
    """Configuração para geração de imagens."""

    model_name: str = "gemini-2.5-flash-image"
    number_of_images: int = 1
    prompt_prefix: str = "Uma foto realista de alta qualidade de:"
    prompt_suffix: str = "Sem texto ou logos na imagem. A casa deve obrigatoriamente possuir uma arquitetura baseada nas casas do Brasil."


@dataclass(frozen=True)
class RAGConfig:
    """Configuração para o pipeline RAG."""

    llm: LLMConfig
    embedding: EmbeddingConfig

    @classmethod
    def default(cls) -> "RAGConfig":
        """Cria configuração padrão para RAG."""
        return cls(llm=LLMConfig(), embedding=EmbeddingConfig())


@dataclass(frozen=True)
class AIConfig:
    """Configuração agregada para todos os componentes de IA."""

    rag: RAGConfig
    image_generation: ImageGenerationConfig
    agent_llm: LLMConfig

    @classmethod
    def default(cls) -> "AIConfig":
        """Cria configuração padrão completa."""
        return cls(
            rag=RAGConfig.default(), image_generation=ImageGenerationConfig(), agent_llm=LLMConfig()
        )


DEFAULT_AI_CONFIG = AIConfig.default()
