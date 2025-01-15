import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .user import User


class Application(Base):
    """
    Модель заявки

    ## Attrs:
        - id: int - идентификатор
        - uid: UUID - идентификатор
        - сreated_at: datetime -
            время и дата создания заявки
        - description: str - описание
        - author_id: int - идентификатор
           пользоватлеля сделавшего заявку
           FK User
        - author: User - связь пользователь
            сдкелавший заявку
    """

    __tablename__ = "application"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    description: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE")
    )
    author: Mapped["User"] = relationship(
        "User", back_populates="applications"
    )
