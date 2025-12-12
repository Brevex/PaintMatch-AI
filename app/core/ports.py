"""
Interfaces (Ports) para inversão de dependências.

Este módulo define os contratos (protocols) que permitem
desacoplar a lógica de negócio das implementações concretas,
seguindo o Dependency Inversion Principle (DIP).
"""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class PaintData:
    """Representação de dados de uma tinta para o domínio."""

    name: str
    color: str
    surface_type: str | None = None
    environment: str | None = None
    finish_type: str | None = None
    features: str | None = None
    line: str | None = None

    def to_document_text(self) -> str:
        """Converte para texto de documento para indexação."""
        return (
            f"Nome: {self.name}. "
            f"Características: {self.features or 'N/A'}. "
            f"Ambiente: {self.environment or 'N/A'}. "
            f"Acabamento: {self.finish_type or 'N/A'}."
        )


class PaintRepository(Protocol):
    """Interface para acesso a dados de tintas."""

    def get_all_paints(self) -> list[PaintData]:
        """Retorna todas as tintas disponíveis."""
        ...


class ImageGenerator(Protocol):
    """Interface para geração de imagens."""

    def generate(self, description: str) -> str:
        """
        Gera uma imagem baseada na descrição.

        Args:
            description: Descrição textual do que gerar

        Returns:
            Mensagem de sucesso ou URL da imagem gerada
        """
        ...


class VectorStoreBuilder(Protocol):
    """Interface para construção de vector stores."""

    def build(self, documents: list[str], metadatas: list[dict]) -> object:
        """
        Constrói um vector store a partir de documentos.

        Args:
            documents: Lista de textos para indexar
            metadatas: Metadados associados a cada documento

        Returns:
            Objeto vector store com método as_retriever()
        """
        ...
