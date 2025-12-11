"""
Repositório de tintas usando SQLAlchemy.

Implementa a interface PaintRepository para acesso ao banco de dados.
"""

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.core import PaintData
from app.db import engine as default_engine
from app.models import Paint


class SqlAlchemyPaintRepository:
    """Implementação de PaintRepository usando SQLAlchemy."""

    def __init__(self, db_engine: Engine | None = None) -> None:
        """Inicializa o repositório."""
        self._engine = db_engine or default_engine

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

        except Exception as e:
            print(
                f"Aviso: Não foi possível ler a tabela 'paints'. "
                f"O banco de dados pode estar vazio ou a tabela não existe. Erro: {e}"
            )
            return []
