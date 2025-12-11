from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.crud import crud_paint
from app.schemas import paint as paint_schema
from app.schemas import user as user_schema

router = APIRouter()


@router.post("/", response_model=paint_schema.Paint, status_code=status.HTTP_201_CREATED)
def create_paint(
    *,
    db: Session = Depends(deps.get_db),
    paint_in: paint_schema.PaintCreate,
    current_user: user_schema.User = Depends(deps.get_current_user),
):
    """
    Cria uma nova tinta (requer autenticação).
    """
    paint = crud_paint.create_paint(db=db, paint=paint_in)
    return paint


@router.get("/", response_model=list[paint_schema.Paint])
def read_paints(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_schema.User = Depends(deps.get_current_user),
):
    """
    Recupera a lista de tintas (requer autenticação).
    """
    paints = crud_paint.get_paints(db, skip=skip, limit=limit)
    return paints
