from sqlalchemy.orm import Session

from app.models.paint import Paint
from app.schemas.paint import PaintCreate


def get_paint(db: Session, paint_id: int) -> Paint | None:
    """Busca uma tinta pelo seu ID."""
    return db.query(Paint).filter(Paint.id == paint_id).first()


def get_paints(db: Session, skip: int = 0, limit: int = 100) -> list[Paint]:
    """Busca uma lista de tintas com paginação."""
    return db.query(Paint).offset(skip).limit(limit).all()


def create_paint(db: Session, paint: PaintCreate) -> Paint:
    """Cria uma nova tinta no banco de dados."""
    db_paint = Paint(**paint.model_dump())
    db.add(db_paint)
    db.commit()
    db.refresh(db_paint)
    return db_paint
