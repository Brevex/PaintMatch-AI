"""Script to load paint data from CSV to the database."""

import os
import sys

import pandas as pd
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.paint import Paint


def load_data_from_csv(db: Session, csv_path: str):
    """Read data from a CSV file and insert into the paints table using bulk insert."""
    try:
        df = pd.read_csv(csv_path)
        print(f"Reading {len(df)} records from CSV file...")

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
                print(f"Paint '{name}' already exists. Skipping.")

        if new_paints:
            db.bulk_save_objects(new_paints)
            db.commit()
            print(f"Inserted {len(new_paints)} new records!")
        else:
            print("No new records to insert.")

    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()


if __name__ == "__main__":
    CSV_FILE_PATH = "Base_de_Dados_de_Tintas_Suvinil.csv"
    db_session = SessionLocal()
    load_data_from_csv(db_session, CSV_FILE_PATH)
    db_session.close()
