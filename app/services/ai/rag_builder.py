"""
RAG Chain Builder.

Single responsibility: build and configure the RAG chain
for retrieval and generation of paint recommendations.
"""

import hashlib
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.core import PROMPTS, PaintData, RAGBuildError, RAGConfig, get_logger, settings

logger = get_logger(__name__)


def format_docs(docs: list) -> str:
    """Format retrieved documents to be sent to the prompt."""
    return "\n\n".join(
        f"Paint Name: {doc.metadata.get('name', 'N/A')}\n"
        f"Color: {doc.metadata.get('color', 'N/A')}\n"
        f"Features: {doc.metadata.get('features', 'N/A')}\n"
        f"Environment: {doc.metadata.get('environment', 'N/A')}\n"
        f"Finish: {doc.metadata.get('finish_type', 'N/A')}"
        for doc in docs
    )


class RAGChainBuilder:
    """Builder for RAG chains for paint recommendation."""

    CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "vector_cache"

    def __init__(self, config: RAGConfig | None = None) -> None:
        """Initialize builder with vector store cache."""
        self._config = config or RAGConfig.default()
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _compute_data_hash(self, paints: list[PaintData]) -> str:
        """Compute data hash to detect changes."""
        content = "".join(p.to_document_text() for p in paints)
        return hashlib.sha256(content.encode()).hexdigest()[:32]

    def _get_cache_path(self, data_hash: str) -> Path:
        """Return cache path for a given hash."""
        return self.CACHE_DIR / f"faiss_index_{data_hash}"

    def build(self, paints: list[PaintData]) -> object | None:
        """
        Build the RAG chain from paint data.

        Uses disk cache to avoid rebuilding the vector store
        when data has not changed.
        """
        if not paints:
            return None

        try:
            data_hash = self._compute_data_hash(paints)
            cache_path = self._get_cache_path(data_hash)

            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            embedding_model = GoogleGenerativeAIEmbeddings(
                model=self._config.embedding.model_name,
                google_api_key=settings.GOOGLE_API_KEY,
            )

            if cache_path.exists():
                logger.info("Loading vector store from cache: %s", cache_path)
                from langchain_community.vectorstores import FAISS

                vector_store = FAISS.load_local(
                    str(cache_path),
                    embedding_model,
                    allow_dangerous_deserialization=True,
                )
            else:
                logger.info("Building new vector store...")
                documents = [paint.to_document_text() for paint in paints]
                metadatas = [self._paint_to_metadata(paint) for paint in paints]
                from langchain_community.vectorstores import FAISS

                vector_store = FAISS.from_texts(
                    documents,
                    embedding=embedding_model,
                    metadatas=metadatas,
                )
                vector_store.save_local(str(cache_path))
                logger.info("Vector store saved at: %s", cache_path)

            retriever = vector_store.as_retriever()

            prompt = ChatPromptTemplate.from_template(PROMPTS.RAG_TEMPLATE)
            from langchain_google_genai import ChatGoogleGenerativeAI

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

        except OSError as e:
            logger.exception("File I/O error with vector store cache: %s", e)
            raise RAGBuildError(f"Cache file error: {e}") from e
        except Exception as e:
            logger.exception("Error creating vector database (RAG): %s", e)
            return None

    @staticmethod
    def _paint_to_metadata(paint: PaintData) -> dict:
        """Convert PaintData to metadata dictionary."""
        return {
            "name": paint.name,
            "color": paint.color,
            "surface_type": paint.surface_type,
            "environment": paint.environment,
            "finish_type": paint.finish_type,
            "features": paint.features,
            "line": paint.line,
        }
