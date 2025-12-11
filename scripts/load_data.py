import os
import sys

import pandas as pd
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.paint import Paint


def load_data_from_csv(db: Session, csv_path: str):
    """
    Lê dados de um arquivo CSV e os insere na tabela de tintas, evitando duplicatas.
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Lendo {len(df)} registros do arquivo CSV...")

        for _, row in df.iterrows():
            paint_exists = db.query(Paint).filter(Paint.name == row["Nome da tinta"]).first()
            if not paint_exists:
                db_paint = Paint(
                    name=row["Nome da tinta"],
                    color=row["Cor"],
                    surface_type=row.get("Tipo de superfície indicada"),
                    environment=row.get("Ambiente"),
                    finish_type=row.get("Tipo de acabamento"),
                    features=row.get("Features relevantes"),
                    line=row.get("Linha"),
                )
                db.add(db_paint)
            else:
                print(f"Tinta '{row['Nome da tinta']}' já existe. Pulando.")

        db.commit()
        print("Dados carregados com sucesso no banco de dados!")

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
