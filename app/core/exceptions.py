"""
Custom exceptions for PaintMatch-AI.

Provides a hierarchy of domain-specific exceptions for better
error handling and debugging throughout the application.
"""


class PaintMatchError(Exception):
    """
    Base exception for all PaintMatch-AI errors.

    All custom exceptions in the application should inherit from this class
    to allow for consistent error handling.
    """

    def __init__(self, message: str = "An error occurred in PaintMatch-AI") -> None:
        self.message = message
        super().__init__(self.message)


class AIServiceError(PaintMatchError):
    """
    Error in AI service operations.

    Raised when there's a problem with AI-related services like
    the chat agent, RAG chain, or image generation.
    """

    def __init__(self, message: str = "AI service error occurred") -> None:
        super().__init__(message)


class ImageGenerationError(AIServiceError):
    """
    Error generating images.

    Raised when the image generation service fails to produce an image.
    """

    def __init__(self, message: str = "Failed to generate image") -> None:
        super().__init__(message)


class RAGBuildError(AIServiceError):
    """
    Error building RAG chain.

    Raised when the RAG chain cannot be constructed, typically due to
    embedding model issues or vector store problems.
    """

    def __init__(self, message: str = "Failed to build RAG chain") -> None:
        super().__init__(message)


class AgentBuildError(AIServiceError):
    """
    Error building the agent.

    Raised when the agent executor cannot be constructed.
    """

    def __init__(self, message: str = "Failed to build agent") -> None:
        super().__init__(message)


class DatabaseError(PaintMatchError):
    """
    Database operation error.

    Raised when there's a problem with database operations.
    """

    def __init__(self, message: str = "Database operation failed") -> None:
        super().__init__(message)


class PaintNotFoundError(DatabaseError):
    """
    Paint not found in database.

    Raised when a requested paint cannot be found.
    """

    def __init__(self, paint_id: int | None = None) -> None:
        message = f"Paint with id {paint_id} not found" if paint_id else "Paint not found"
        super().__init__(message)


class AuthenticationError(PaintMatchError):
    """
    Authentication error.

    Raised when authentication fails.
    """

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message)


class ValidationError(PaintMatchError):
    """
    Validation error.

    Raised when input validation fails.
    """

    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(message)
