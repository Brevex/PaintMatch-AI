from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import chat as chat_schema
from app.schemas import user as user_schema
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/", response_model=chat_schema.ChatResponse)
def ask_question(
    *,
    db: Session = Depends(deps.get_db),
    current_user: user_schema.User = Depends(deps.get_current_user),
    chat_service: ChatService = Depends(deps.get_chat_service),
    query: chat_schema.ChatQuery,
):
    """
    Endpoint para enviar perguntas ao assistente de IA (requer autenticação).
    Pode retornar uma URL de imagem se uma simulação visual for solicitada.
    """
    response_data = chat_service.get_ai_response(query.question)

    return response_data
