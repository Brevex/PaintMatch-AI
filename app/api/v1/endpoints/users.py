from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.crud import crud_user
from app.schemas import user as user_schema

router = APIRouter()


@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(deps.get_db), user_in: user_schema.UserCreate):
    """
    Create a new user in the system.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    user = crud_user.create_user(db=db, user=user_in)
    return user
