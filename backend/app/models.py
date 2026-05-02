from sqlalchemy import Integer, Text, String, 
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class Admin(Base):
    __tablename__ = "admin"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_has: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    
class About(Base):
    __tablename__ = "about"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    headline: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    profile_image_link: Mapped[str] = mapped_column(Text, nullable=True)
    email_public: Mapped[str] = mapped_column(String(150), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    github_link: Mapped[str] = mapped_column(String(200))
    linkedin_link: Mapped[str] = mapped_column(String(200))
