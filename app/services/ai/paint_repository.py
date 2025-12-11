"""
Repositório de tintas usando SQLAlchemy.

Implementa a interface PaintRepository para acesso ao banco de dados.
"""

import pandas as pd
from sqlalchemy import Engine

from app.core.ports import PaintData
from app.db.session import engine as default_engine


class SqlAlchemyPaintRepository:
    """Implementação de PaintRepository usando SQLAlchemy."""

    def __init__(self, db_engine: Engine | None = None) -> None:
        """
        Inicializa o repositório.

        Args:
            db_engine: Engine SQLAlchemy. Usa engine padrão se não fornecida.
        """
        self._engine = db_engine or default_engine

    def get_all_paints(self) -> list[PaintData]:
        """
        Retorna todas as tintas do banco de dados.

        Returns:
            Lista de PaintData com todas as tintas disponíveis
        """
        try:
            df = pd.read_sql("SELECT * FROM paints", self._engine)

            if df.empty:
                return []

            return [
                PaintData(
                    name=row["name"],
                    color=row["color"],
                    surface_type=row.get("surface_type"),
                    environment=row.get("environment"),
                    finish_type=row.get("finish_type"),
                    features=row.get("features"),
                    line=row.get("line"),
                )
                for _, row in df.iterrows()
            ]

        except Exception as e:
            print(
                f"Aviso: Não foi possível ler a tabela 'paints'. "
                f"O banco de dados pode estar vazio ou a tabela não existe. Erro: {e}"
            )
            return []
