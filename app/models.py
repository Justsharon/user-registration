from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    phone_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    id_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )