from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenData
from app.services.chat_service import ChatService, create_chat_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

_chat_service_instance: ChatService | None = None


def get_chat_service() -> ChatService:
    """
    Factory para obter instância do ChatService.

    Utiliza cache para evitar reconstrução do agente a cada request.
    """
    global _chat_service_instance
    if _chat_service_instance is None:
        _chat_service_instance = create_chat_service()
    return _chat_service_instance


def get_db() -> Generator:
    """
    Função geradora para injeção de dependência da sessão do banco de dados.
    Garante que a sessão seja sempre fechada após a requisição.
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Decodifica o token JWT, valida e retorna o usuário correspondente.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenData(email=payload.get("sub"))
        if token_data.email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
