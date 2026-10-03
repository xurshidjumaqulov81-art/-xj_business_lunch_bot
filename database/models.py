from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telegram_first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telegram_last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    full_name: Mapped[str] = mapped_column(String(255))
    xj_id: Mapped[str] = mapped_column(String(7), index=True)
    phone: Mapped[str] = mapped_column(String(50))

    is_registered_for_launch: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applications: Mapped[list["ContestApplication"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class ContestApplication(Base):
    __tablename__ = "contest_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    about: Mapped[str] = mapped_column(Text)
    goal: Mapped[str] = mapped_column(Text)
    why_founder: Mapped[str] = mapped_column(Text)
    one_question: Mapped[str] = mapped_column(Text)
    after_meeting: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(30), default="pending")
    admin_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="applications")

