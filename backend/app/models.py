from sqlalchemy import String, Text ,Integer
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class User(Base):
    __tablename__ = "admin"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(130), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

class About(Base):
    __tablename__ = "about"
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_link: Mapped[str] = mapped_column(Text, nullable=False)
    
class TechStack(Base):
    __tablename__ = "tech_stack"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    languages: Mapped[str] = mapped_column(String(150), nullable=False)
    framework: Mapped[str] = mapped_column(String(150), nullable=False)
    tools: Mapped[str] = mapped_column(String(150), nullable=False)
    databases: Mapped[str] = mapped_column(String(150), nullable=False)

class Education(Base):
    __tablename__ = "education"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[str] = mapped_column(String(5))
    end_date: Mapped[str] = mapped_column(String(5), default="present")