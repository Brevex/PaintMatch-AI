from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1 import deps
from app.core import AIServiceError, get_logger
from app.schemas import chat as chat_schema
from app.schemas import user as user_schema
from app.services.chat_service import ChatService

router = APIRouter()
logger = get_logger(__name__)


@router.post("/", response_model=chat_schema.ChatResponse)
def ask_question(
    *,
    current_user: user_schema.User = Depends(deps.get_current_user),
    chat_service: ChatService = Depends(deps.get_chat_service),
    query: chat_schema.ChatQuery,
):
    """
    Endpoint para enviar perguntas ao assistente de IA (requer autenticação).
    Pode retornar uma URL de imagem se uma simulação visual for solicitada.
    """
    try:
        response_data = chat_service.get_ai_response(query.question)
        return response_data
    except AIServiceError as e:
        logger.error("AI service error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="O serviço de IA está temporariamente indisponível. Tente novamente.",
        ) from e
    except Exception as e:
        logger.exception("Unexpected error in chat endpoint: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno. Por favor, tente novamente.",
        ) from e
