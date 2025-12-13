"""
Paint Repository using SQLAlchemy.

Implements PaintRepository interface for database access.
"""

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import PaintData, get_logger
from app.models import Paint

logger = get_logger(__name__)


class SqlAlchemyPaintRepository:
    """PaintRepository implementation using SQLAlchemy."""

    def __init__(self, db_engine: Engine | None = None) -> None:
        """
        Initialize the repository.

        Args:
            db_engine: SQLAlchemy Engine. If None, uses default engine.
        """
        if db_engine is None:
            # Lazy import to avoid circular dependency
            from app.db import engine as default_engine

            db_engine = default_engine
        self._engine = db_engine

    def get_all_paints(self) -> list[PaintData]:
        """Return all paints from the database using native SQLAlchemy."""
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
