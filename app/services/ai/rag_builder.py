"""
Construtor da RAG Chain.

Responsabilidade única: construir e configurar a cadeia RAG
para recuperação e geração de recomendações de tintas.
"""

import hashlib
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from app.core.config import settings
from app.core.llm_config import RAGConfig
from app.core.ports import PaintData
from app.core.prompts import PROMPTS


def format_docs(docs: list) -> str:
    """Formata os documentos recuperados para serem enviados ao prompt."""
    return "\n\n".join(
        f"Nome da Tinta: {doc.metadata.get('name', 'N/A')}\n"
        f"Cor: {doc.metadata.get('color', 'N/A')}\n"
        f"Características: {doc.metadata.get('features', 'N/A')}\n"
        f"Ambiente: {doc.metadata.get('environment', 'N/A')}\n"
        f"Acabamento: {doc.metadata.get('finish_type', 'N/A')}"
        for doc in docs
    )


class RAGChainBuilder:
    """Construtor de cadeias RAG para recomendação de tintas."""

    CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "vector_cache"

    def __init__(self, config: RAGConfig | None = None) -> None:
        """Inicializa o construtor com cache de vector store."""
        self._config = config or RAGConfig.default()
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _compute_data_hash(self, paints: list[PaintData]) -> str:
        """Computa hash dos dados para detectar mudanças."""
        content = "".join(p.to_document_text() for p in paints)
        return hashlib.md5(content.encode()).hexdigest()

    def _get_cache_path(self, data_hash: str) -> Path:
        """Retorna o caminho do cache para um dado hash."""
        return self.CACHE_DIR / f"faiss_index_{data_hash}"

    def build(self, paints: list[PaintData]) -> object | None:
        """
        Constrói a cadeia RAG a partir dos dados de tintas.

        Utiliza cache em disco para evitar reconstrução do vector store
        quando os dados não mudaram.
        """
        if not paints:
            return None

        try:
            data_hash = self._compute_data_hash(paints)
            cache_path = self._get_cache_path(data_hash)

            embedding_model = GoogleGenerativeAIEmbeddings(
                model=self._config.embedding.model_name,
                google_api_key=settings.GOOGLE_API_KEY,
            )

            if cache_path.exists():
                print(f"Carregando vector store do cache: {cache_path}")
                vector_store = FAISS.load_local(
                    str(cache_path),
                    embedding_model,
                    allow_dangerous_deserialization=True,
                )
            else:
                print("Construindo novo vector store...")
                documents = [paint.to_document_text() for paint in paints]
                metadatas = [self._paint_to_metadata(paint) for paint in paints]

                vector_store = FAISS.from_texts(
                    documents,
                    embedding=embedding_model,
                    metadatas=metadatas,
                )
                vector_store.save_local(str(cache_path))
                print(f"Vector store salvo em: {cache_path}")

            retriever = vector_store.as_retriever()

            prompt = ChatPromptTemplate.from_template(PROMPTS.RAG_TEMPLATE)
            llm = ChatGoogleGenerativeAI(
                model=self._config.llm.model_name,
                temperature=self._config.llm.temperature,
                google_api_key=settings.GOOGLE_API_KEY,
            )

            return (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

        except Exception as e:
            print(f"Erro ao criar base vetorial (RAG): {e}")
            return None

    def _paint_to_metadata(self, paint: PaintData) -> dict:
        """Converte PaintData para dicionário de metadados."""
        return {
            "name": paint.name,
            "color": paint.color,
            "surface_type": paint.surface_type,
            "environment": paint.environment,
            "finish_type": paint.finish_type,
            "features": paint.features,
            "line": paint.line,
        }
