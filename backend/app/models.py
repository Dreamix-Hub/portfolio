from sqlalchemy import Integer, Text, String, 
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class Admin(Base):
    __tablename__ = "admin"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_has: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    

