from models.base import Base
from sqlalchemy import String, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column

class LanguageModel(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[str] = mapped_column(String(5), nullable=False)

    UniqueConstraint("code")

    def as_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "id": self.id
        }
