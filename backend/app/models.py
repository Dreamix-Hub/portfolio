from __future__ import annotations

from sqlalchemy import Integer, Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Admin(Base):
    __tablename__ = "admin"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    
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
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_has: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
  
class ProjectCategory(Base):
    __tablename__ = "project_category"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)    
    project: Mapped[Project] = relationship(back_populates="project_category")  # <---- 1-to-M relationship with project
    
class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    live_link: Mapped[str] = mapped_column(Text, nullable=True)
    github_link: Mapped[str] = mapped_column(Text, nullable=True)
    featured: Mapped[bool | None] = mapped_column(default=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("project_category.id"),
        nullable=False,
        index=True
    )
    project_category: Mapped[ProjectCategory] = relationship(back_populates="projects") # <---- M-to-1 relationship with project_category

