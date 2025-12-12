from pydantic import BaseModel


class ChatQuery(BaseModel):
    """Schema for chat query input."""

    question: str


class ChatResponse(BaseModel):
    """Schema for chat response output."""

    answer: str
    image_url: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary (alias for model_dump for compatibility)."""
        return self.model_dump()
