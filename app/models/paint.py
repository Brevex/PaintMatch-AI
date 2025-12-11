from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Paint(Base):
    __tablename__ = "paints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, nullable=False)
    surface_type = Column(String)
    environment = Column(String)
    finish_type = Column(String)
    features = Column(String)
    line = Column(String)
