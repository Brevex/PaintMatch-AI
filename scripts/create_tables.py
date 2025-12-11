import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine
from app.models.paint import Paint  # noqa: F401
from app.models.user import User  # noqa: F401


def create_database_tables():
    """
    Cria todas as tabelas no banco de dados definidas nos modelos.
    """
    print("Iniciando a criação das tabelas no banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas 'users' e 'paints' criadas com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao criar as tabelas: {e}")


if __name__ == "__main__":
    create_database_tables()
