from models.base import Base
from sqlalchemy import String, ForeignKey, UniqueConstraint, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class EntryModel(Base):
    __tablename__ = 'entries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(30))
    value: Mapped[str] = mapped_column(String(50), nullable=True)
    parent: Mapped[int] = mapped_column(Integer, ForeignKey("entries.id"), nullable=True)
    namespace_id: Mapped[int] = mapped_column(Integer, ForeignKey("namespaces.id"), nullable=False)

    UniqueConstraint("parent", "key"),
