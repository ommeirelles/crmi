from models.base import Base
from sqlalchemy import String, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

class LanguageModel(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(SmallInteger,primary_key=True, autoincrement=True,)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[str] = mapped_column(String(5), nullable=False)

    UniqueConstraint("code")