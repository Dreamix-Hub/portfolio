from pydantic import BaseModel, ConfigDict, EmailStr, Field

from typing import Optional
from datetime import datetime
class AdminBase(BaseModel):
    username: str = Field(min_length=4)

class AdminLogin(AdminBase):
    password: str = Field(min_length=8)

class AdminResponse(AdminBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
class AdminCreate(AdminLogin):
    pass

class Token:
    token_type: str
    access_token: str
    
class ProjectCreate(BaseModel):
    title: str = Field(min_length=5)
    description: str = Field(min_length=10)
    live_link: Optional[str] = None
    github_link: Optional[str] = None
    featured: bool = Field(default=False)
    category_id: int 
    techstack_ids: list[int]

class ProjectUpdate(BaseModel):
    title: Optional[str] = None 
    description: Optional[str] = None 
    live_link: Optional[str] = None
    github_link: Optional[str] = None
    featured: bool = Field(default=False)
    category_id: int 
    techstack_ids: Optional[list[int]] = None 
   
class CategorySchema(BaseModel):
    id: int
    category_name: str 
class ProjectCategorySchema(CategorySchema):
    pass
class TechStackSchema(BaseModel):
    id: int
    name: str
    type: str
    
class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : int
    title: str
    description: str
    category: ProjectCategorySchema
    techstacks: list[TechStackSchema]
    live_link: str
    github_link: str
    featured: bool

class BlogCreate(BaseModel):
    title: str = Field(min_length=5)
    content: str = Field(min_length=10)
    is_draft: bool = Field(default=False)
    category_id: int 

class BlogUpdate(BaseModel):
    title: str | None = Field(default=None ,min_length=5)
    content: str | None = Field(default=None, min_length=10)
    is_draft: bool = Field(default=False)
    category_id: int | None

class BlogCategorySchema(CategorySchema):
   pass
class BlogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    content: str
    category: BlogCategorySchema
    is_draft: bool
    created_at: datetime
    updated_at: datetime
    