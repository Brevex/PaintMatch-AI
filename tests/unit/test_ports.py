"""
Unit tests for app/core/ports.py

Tests domain data classes and their methods following
AAA pattern (Arrange-Act-Assert) and FIRST principles.
"""

from app.core import ChatResponse, PaintData


class TestPaintData:
    """Tests for PaintData dataclass."""

    def test_paint_data_to_document_text(self, sample_paint_data):
        """Test that to_document_text formats correctly with all fields."""
        # ARRANGE - fixture provides sample_paint_data

        # ACT
        document_text = sample_paint_data.to_document_text()

        # ASSERT
        assert "Nome: Suvinil Toque de Seda" in document_text
        assert "Características: Lavável, antimofo" in document_text
        assert "Ambiente: Interno" in document_text
        assert "Acabamento: Acetinado" in document_text

    def test_paint_data_to_document_text_with_none_values(self, paint_data_with_none_values):
        """Edge case: to_document_text handles None values as 'N/A'."""
        # ARRANGE - fixture provides paint_data_with_none_values

        # ACT
        document_text = paint_data_with_none_values.to_document_text()

        # ASSERT
        assert "Nome: Tinta Básica" in document_text
        assert "Características: N/A" in document_text
        assert "Ambiente: N/A" in document_text
        assert "Acabamento: N/A" in document_text

    def test_paint_data_creation_with_minimal_fields(self):
        """Test PaintData creation with only required fields."""
        # ARRANGE & ACT
        paint = PaintData(name="Tinta Simples", color="Azul")

        # ASSERT
        assert paint.name == "Tinta Simples"
        assert paint.color == "Azul"
        assert paint.surface_type is None
        assert paint.environment is None


class TestChatResponse:
    """Tests for ChatResponse dataclass."""

    def test_chat_response_to_dict(self, chat_response_with_image):
        """Test that to_dict serializes correctly with image_url."""
        # ARRANGE - fixture provides chat_response_with_image

        # ACT
        result = chat_response_with_image.to_dict()

        # ASSERT
        assert isinstance(result, dict)
        assert result["answer"] == "Recomendo a tinta Suvinil Acrílico para sua parede externa."
        assert result["image_url"] == "http://localhost:8000/static/images/test-image.png"

    def test_chat_response_to_dict_without_image(self, chat_response_without_image):
        """Edge case: to_dict handles None image_url correctly."""
        # ARRANGE - fixture provides chat_response_without_image

        # ACT
        result = chat_response_without_image.to_dict()

        # ASSERT
        assert isinstance(result, dict)
        assert result["answer"] == "Recomendo a tinta Suvinil Acrílico para sua parede externa."
        assert result["image_url"] is None

    def test_chat_response_creation_defaults(self):
        """Test ChatResponse creation with default image_url."""
        # ARRANGE & ACT
        response = ChatResponse(answer="Resposta de teste")

        # ASSERT
        assert response.answer == "Resposta de teste"
        assert response.image_url is None
