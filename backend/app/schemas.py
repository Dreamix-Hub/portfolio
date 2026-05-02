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
    description = Field(min_length=10)
    category_id: int 
    techstack_ids: list[int]
    live_link: Optional[str] = None
    github_link: Optional[str] = None
    featured: Optional[bool] = Field(default=False)

