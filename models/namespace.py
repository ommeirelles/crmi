from models.base import Base
from sqlalchemy import String, SmallInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

class NamespaceModel(Base):
    __tablename__ = 'namespaces'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    language_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("languages.id"), nullable=False)
    
    UniqueConstraint("language_id", "name")
