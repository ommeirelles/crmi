from models.base import Base
from sqlalchemy import String, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column

class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(65), nullable=False)

    UniqueConstraint("login")

    def as_dict(self) -> dict:
        return {
            "login": self.login,
            "id": self.id
        }
