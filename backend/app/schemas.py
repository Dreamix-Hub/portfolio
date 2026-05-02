from pydantic import BaseModel, ConfigDict, EmailStr, Field

from typing import Optional
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
    featured: Optional[bool] = Field(default=False)
    category_id: int 
    techstack_ids: list[int]

class ProjectUpdate(BaseModel):
    title: Optional[str] = None 
    description: Optional[str] = None 
    live_link: Optional[str] = None
    github_link: Optional[str] = None
    featured: Optional[bool] = Field(default=False)
    category_id: int 
    techstack_ids: Optional[list[int]] = None 
    
class ProjectCategorySchema(BaseModel):
    id: int
    category_name: str

class TechStackSchema(BaseModel):
    id: int
    name: str
    type: str
    
class ProjectResponse(BaseModel):
    id : int
    title: str
    description: str
    category: ProjectCategorySchema
    techstacks: list[TechStackSchema]
    live_link: str
    github_link: str
    featured: bool
