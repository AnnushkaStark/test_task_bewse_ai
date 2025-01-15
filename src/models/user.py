import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .application import Application


class User(Base):
    """
    Модель пользователя

    ## Attrs:
        - id: int - идентификатор
        - uid: UUID - идентификатор
        - username: str - юзеренйм
        - email: str - электронная почта
        - password: str - пароль пользователя
        - applications: List[Application] - связь
            заявки сделанные пользователем
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, index=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str]
    applications: Mapped[List["Application"]] = relationship(
        "Application", back_populates="author"
    )
