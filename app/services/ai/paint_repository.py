"""
Repositório de tintas usando SQLAlchemy.

Implementa a interface PaintRepository para acesso ao banco de dados.
"""

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import PaintData, get_logger
from app.models import Paint

logger = get_logger(__name__)


class SqlAlchemyPaintRepository:
    """Implementação de PaintRepository usando SQLAlchemy."""

    def __init__(self, db_engine: Engine | None = None) -> None:
        """
        Inicializa o repositório.

        Args:
            db_engine: Engine do SQLAlchemy. Se None, usa a engine padrão.
        """
        if db_engine is None:
            # Lazy import para evitar dependência circular
            from app.db import engine as default_engine

            db_engine = default_engine
        self._engine = db_engine

    def get_all_paints(self) -> list[PaintData]:
        """Retorna todas as tintas do banco de dados usando SQLAlchemy nativo."""
        try:
            with Session(self._engine) as session:
                paints = session.query(Paint).all()

                if not paints:
                    return []

                return [
                    PaintData(
                        name=paint.name,
                        color=paint.color,
                        surface_type=paint.surface_type,
                        environment=paint.environment,
                        finish_type=paint.finish_type,
                        features=paint.features,
                        line=paint.line,
                    )
                    for paint in paints
                ]

        except SQLAlchemyError as e:
            logger.warning(
                "Database error reading 'paints' table: %s",
                e,
            )
            return []
        except Exception as e:
            logger.warning(
                "Unexpected error reading 'paints' table: %s",
                e,
            )
            return []
