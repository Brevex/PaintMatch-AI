"""
Unit tests for app/services/chat_service.py

Tests ChatService class and its methods following
AAA pattern (Arrange-Act-Assert) and FIRST principles.
Uses mocks to isolate from external dependencies.
"""

from unittest.mock import MagicMock, patch

from app.services.chat_service import ChatService, create_chat_service


class TestChatServiceURLExtraction:
    """Tests for _extract_url private method."""

    def test_extract_url_with_valid_http_url(self):
        """Test URL extraction from text containing http URL."""
        # ARRANGE
        with patch.object(ChatService, "__init__", lambda self, **kwargs: None):
            service = ChatService()
            service._config = None
            service._paint_repository = None
            service._image_generator = None
            service._agent_executor = None
        text = "A imagem foi gerada com sucesso! Veja: http://localhost:8000/static/images/abc.png"

        # ACT
        result = service._extract_url(text)

        # ASSERT
        assert result == "http://localhost:8000/static/images/abc.png"

    def test_extract_url_with_valid_https_url(self):
        """Test URL extraction from text containing https URL."""
        # ARRANGE
        with patch.object(ChatService, "__init__", lambda self, **kwargs: None):
            service = ChatService()
            service._config = None
            service._paint_repository = None
            service._image_generator = None
            service._agent_executor = None
        text = "Acesse: https://example.com/image.jpg para ver a imagem."

        # ACT
        result = service._extract_url(text)

        # ASSERT
        assert result == "https://example.com/image.jpg"

    def test_extract_url_without_url(self):
        """Edge case: returns None when text contains no URL."""
        # ARRANGE
        with patch.object(ChatService, "__init__", lambda self, **kwargs: None):
            service = ChatService()
            service._config = None
            service._paint_repository = None
            service._image_generator = None
            service._agent_executor = None
        text = "Esta é uma resposta sem nenhuma URL."

        # ACT
        result = service._extract_url(text)

        # ASSERT
        assert result is None


class TestChatServiceGetAIResponse:
    """Tests for get_ai_response method."""

    def test_get_ai_response_returns_error_when_no_agent(self):
        """Failure case: returns error message when agent is not initialized."""
        # ARRANGE
        with patch.object(ChatService, "__init__", lambda self, **kwargs: None):
            service = ChatService()
            service._config = None
            service._paint_repository = MagicMock()
            service._paint_repository.get_all_paints.return_value = []
            service._image_generator = None
            service._agent_executor = None

        # ACT
        result = service.get_ai_response("Qual a melhor tinta?")

        # ASSERT
        assert "answer" in result
        assert "inicializando" in result["answer"] or "vazio" in result["answer"]

    def test_get_ai_response_handles_agent_exception(self):
        """Failure case: handles exception during agent invocation gracefully."""
        # ARRANGE
        with patch.object(ChatService, "__init__", lambda self, **kwargs: None):
            service = ChatService()
            service._config = None
            service._paint_repository = None
            service._image_generator = None

            mock_agent = MagicMock()
            mock_agent.invoke.side_effect = Exception("Agent error")
            service._agent_executor = mock_agent

        # ACT
        result = service.get_ai_response("Qual a melhor tinta?")

        # ASSERT
        assert "answer" in result
        assert "erro" in result["answer"].lower()


class TestCreateChatServiceFactory:
    """Tests for create_chat_service factory function."""

    def test_create_chat_service_returns_instance(self):
        """Test that factory returns ChatService instance."""
        # ARRANGE & ACT
        with patch.object(ChatService, "__init__", lambda self, **kwargs: None):
            service = create_chat_service()

        # ASSERT
        assert isinstance(service, ChatService)
