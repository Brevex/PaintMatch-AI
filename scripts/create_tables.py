import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine
from app.models.paint import Paint  # noqa: F401
from app.models.user import User  # noqa: F401


def create_database_tables():
    """
    Create all tables in the database defined in the models.
    """
    print("Starting database table creation...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables 'users' and 'paints' created successfully!")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")


if __name__ == "__main__":
    create_database_tables()
