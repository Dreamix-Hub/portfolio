from __future__ import annotations

from sqlalchemy import Integer, Text, String, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List
from datetime import datetime, UTC

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
    profile_image_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    email_public:Mapped[str | None] = mapped_column(String(150), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    github_link: Mapped[str] = mapped_column(String(200))
    linkedin_link: Mapped[str] = mapped_column(String(200))
  
# association table for using in Many-to-many relationship 
project_techstack = Table(
    "project_techstack", # <-- table name
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("techstack_id", ForeignKey("tech_stacks.id"), primary_key=True)
)

class ProjectCategory(Base):
    __tablename__ = "project_categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)    
    project: Mapped[List["Project"]] = relationship(back_populates="project_categories")  # <---- 1-to-M relationship with project
    
class TechStack(Base):
    __tablename__ = "tech_stacks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    projects: Mapped[List["Project"]] = relationship(
        secondary="project_techstack",
        back_populates="tech_stacks"
    )
class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    live_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    github_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    featured: Mapped[bool | None] = mapped_column(default=False)
    
    category_id: Mapped[int] = mapped_column(
        ForeignKey("project_categories.id"),
        nullable=False,
        index=True
    )
    category: Mapped[ProjectCategory] = relationship(back_populates="projects") # <---- M-to-1 relationship with project_category
    
    techstack: Mapped[List["TechStack"]] = relationship(
        secondary="project_techstack",
        back_populates="projects"
    )
    
class BlogCategory(Base):
    __tablename__ = "blog_categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    blog: Mapped[List["Blog"]] = relationship(back_populates="blog_category")
    
class Blog(Base):
    __tablename__ = "blogs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_draft: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(UTC))
    
    category_id: Mapped[int] = mapped_column(
        ForeignKey("blog_category.id"),
        nullable=False,
        index=True
    )
    category: Mapped[BlogCategory] = relationship(back_populates="blogs") 

