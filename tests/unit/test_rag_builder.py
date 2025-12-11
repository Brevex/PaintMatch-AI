"""
Unit tests for app/services/ai/rag_builder.py

Tests RAGChainBuilder class and format_docs function following
AAA pattern (Arrange-Act-Assert) and FIRST principles.
"""

from app.core import PaintData, RAGConfig
from app.services.ai import RAGChainBuilder
from app.services.ai.rag_builder import format_docs


class TestFormatDocs:
    """Tests for format_docs function."""

    def test_format_docs_formats_correctly(self):
        """Test that documents are formatted with correct template."""

        # ARRANGE
        class MockDoc:
            def __init__(self, metadata):
                self.metadata = metadata

        docs = [
            MockDoc(
                {
                    "name": "Suvinil Acrílico",
                    "color": "Branco",
                    "features": "Lavável",
                    "environment": "Interno",
                    "finish_type": "Fosco",
                }
            )
        ]

        # ACT
        result = format_docs(docs)

        # ASSERT
        assert "Nome da Tinta: Suvinil Acrílico" in result
        assert "Cor: Branco" in result
        assert "Características: Lavável" in result
        assert "Ambiente: Interno" in result
        assert "Acabamento: Fosco" in result

    def test_format_docs_handles_missing_metadata(self):
        """Edge case: handles missing metadata fields with N/A."""

        # ARRANGE
        class MockDoc:
            def __init__(self, metadata):
                self.metadata = metadata

        docs = [MockDoc({})]

        # ACT
        result = format_docs(docs)

        # ASSERT
        assert "Nome da Tinta: N/A" in result
        assert "Cor: N/A" in result

    def test_format_docs_multiple_documents(self):
        """Test formatting multiple documents with separator."""

        # ARRANGE
        class MockDoc:
            def __init__(self, metadata):
                self.metadata = metadata

        docs = [
            MockDoc({"name": "Tinta 1", "color": "Azul"}),
            MockDoc({"name": "Tinta 2", "color": "Verde"}),
        ]

        # ACT
        result = format_docs(docs)

        # ASSERT
        assert "Tinta 1" in result
        assert "Tinta 2" in result
        assert "\n\n" in result


class TestRAGChainBuilder:
    """Tests for RAGChainBuilder class."""

    def test_build_returns_none_for_empty_paints(self):
        """Edge case: build returns None when paint list is empty."""
        # ARRANGE
        builder = RAGChainBuilder()
        empty_paints: list[PaintData] = []

        # ACT
        result = builder.build(empty_paints)

        # ASSERT
        assert result is None

    def test_paint_to_metadata_conversion(self):
        """Test that PaintData is correctly converted to metadata dict."""
        # ARRANGE
        builder = RAGChainBuilder()
        paint = PaintData(
            name="Suvinil Premium",
            color="Azul Celeste",
            surface_type="Parede",
            environment="Externo",
            finish_type="Acetinado",
            features="Antimofo",
            line="Premium",
        )

        # ACT
        result = builder._paint_to_metadata(paint)

        # ASSERT
        assert result["name"] == "Suvinil Premium"
        assert result["color"] == "Azul Celeste"
        assert result["surface_type"] == "Parede"
        assert result["environment"] == "Externo"
        assert result["finish_type"] == "Acetinado"
        assert result["features"] == "Antimofo"
        assert result["line"] == "Premium"

    def test_paint_to_metadata_with_none_values(self):
        """Test metadata conversion with None optional fields."""
        # ARRANGE
        builder = RAGChainBuilder()
        paint = PaintData(
            name="Tinta Básica",
            color="Branco",
            surface_type=None,
            environment=None,
        )

        # ACT
        result = builder._paint_to_metadata(paint)

        # ASSERT
        assert result["name"] == "Tinta Básica"
        assert result["color"] == "Branco"
        assert result["surface_type"] is None
        assert result["environment"] is None

    def test_rag_chain_builder_uses_config(self):
        """Test that builder accepts and stores configuration."""
        # ARRANGE
        config = RAGConfig.default()

        # ACT
        builder = RAGChainBuilder(config=config)

        # ASSERT
        assert builder._config == config
