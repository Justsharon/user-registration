from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLookup, UserLookupResponse, UserResponse

router = APIRouter()


@router.post("/lookup", response_model=UserLookupResponse)
def lookup_user(payload: UserLookup, db: Session = Depends(get_db)):
    statement = select(User).where(User.phone_number == payload.phone_number)
    user = db.scalar(statement)
    if user:
        return UserLookupResponse(registered=True, message="User found")

    return UserLookupResponse(registered=False, message="User not found")


@router.post("/register", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # 1. Create a SQLAlchemy User object
    user = User(
        phone_number=payload.phone_number,
        full_name=payload.full_name,
        email=payload.email,
        id_number=payload.id_number,
    )

    # 2. Add it to the session
    db.add(user)

    # 3. Commit the transaction
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Phone number or ID number already exists"
        )

    return UserResponse(success=True, message="Registration successful")
