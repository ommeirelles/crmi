from models.base import Base
from sqlalchemy import String, ForeignKey, UniqueConstraint, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class SessionModel(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(65), nullable=False)
    
    UniqueConstraint("user_id")
    UniqueConstraint("token")
