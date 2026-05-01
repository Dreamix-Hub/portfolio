from datetime import datetime, UTC

from sqlalchemy import String, Text ,Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    
class Author(BaseModel):
    __tablename__ = "admin"
    
    email: Mapped[str] = mapped_column(String(130), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

class About(BaseModel):
    __tablename__ = "about"
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_link: Mapped[str] = mapped_column(Text, nullable=False)
    
class TechStack(BaseModel):
    __tablename__ = "tech_stack"
    
    languages: Mapped[str] = mapped_column(String(150), nullable=False)
    framework: Mapped[str] = mapped_column(String(150), nullable=False)
    tools: Mapped[str] = mapped_column(String(150), nullable=False)
    databases: Mapped[str] = mapped_column(String(150), nullable=False)

class Education(BaseModel):
    __tablename__ = "education"
    
    title: Mapped[str] = mapped_column(Text, nullable=False)
    institute: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[str] = mapped_column(String(5))
    end_date: Mapped[str] | None = mapped_column(String(5), default="present")

class Project(BaseModel):
    __tablename__ = "projects"
    
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    category_tag: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    techstack_tags: Mapped[str] = mapped_column(Text, nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean)
    live_link: Mapped[str] = mapped_column(Text)
    github_link: Mapped[str] = mapped_column(Text)
        
class Blog(BaseModel):
    __tablename__ = "blogs"
    
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    tags: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    cover_image_link: Mapped[str] = mapped_column(Text, nullable=True)# optional
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )
    drafted: Mapped[bool] = mapped_column(Boolean)

class Contact(BaseModel):
    __tablename__ = "contact_form"
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    subject: Mapped[str] = mapped_column(String(250), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    read: Mapped[bool] = mapped_column(Boolean)
    