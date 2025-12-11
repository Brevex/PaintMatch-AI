"""Script para carregar dados de tintas do CSV para o banco de dados."""

import os
import sys

import pandas as pd
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.paint import Paint


def load_data_from_csv(db: Session, csv_path: str):
    """Lê dados de um arquivo CSV e os insere na tabela de tintas usando bulk insert."""
    try:
        df = pd.read_csv(csv_path)
        print(f"Lendo {len(df)} registros do arquivo CSV...")

        existing_names = {name for (name,) in db.query(Paint.name).all()}

        new_paints = []
        for record in df.to_dict("records"):
            name = record["Nome da tinta"]
            if name not in existing_names:
                new_paints.append(
                    Paint(
                        name=name,
                        color=record["Cor"],
                        surface_type=record.get("Tipo de superfície indicada"),
                        environment=record.get("Ambiente"),
                        finish_type=record.get("Tipo de acabamento"),
                        features=record.get("Features relevantes"),
                        line=record.get("Linha"),
                    )
                )
            else:
                print(f"Tinta '{name}' já existe. Pulando.")

        if new_paints:
            db.bulk_save_objects(new_paints)
            db.commit()
            print(f"Inseridos {len(new_paints)} registros novos!")
        else:
            print("Nenhum registro novo para inserir.")

    except FileNotFoundError:
        print(f"Erro: O arquivo {csv_path} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()


if __name__ == "__main__":
    CSV_FILE_PATH = "Base_de_Dados_de_Tintas_Suvinil.csv"
    db_session = SessionLocal()
    load_data_from_csv(db_session, CSV_FILE_PATH)
    db_session.close()
