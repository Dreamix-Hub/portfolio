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
    access_token: str
    token_type: str
    
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

class ProjectCategoryCreate(BaseModel):
    category_name: str 
class ProjectCategoryUpdate(BaseModel):
    category_name: str | None = Field(default=None)
class ProjectCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: str 
    
class TechStackCreate(BaseModel):
    name: str
    type: str
class TechStackUpdate(BaseModel):
    name: str | None = Field(default=None)
    type: str | None = Field(default=None)

class TechStackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    
class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : int
    title: str
    description: str
    category: ProjectCategoryResponse
    techstacks: list[TechStackResponse]
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
    category_id: int | None = Field(default=None)

class BlogCategoryCreate(BaseModel):
    category_name: str
class BlogCategoryUpdate(BaseModel):
    category_name: str | None = Field(default=None)
class BlogCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: str 
class BlogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    content: str
    category: BlogCategoryResponse
    is_draft: bool
    created_at: datetime
    updated_at: datetime
    
class EducationBase(BaseModel):
    title: str
    institute: str
    start_date: datetime
    end_date: datetime

class EducationCreate(EducationBase):
    pass

class EducationResponse(EducationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
class EducationUpdate(BaseModel):
    title: str | None = Field(default=None)
    institute: str | None = Field(default=None)
    start_date: datetime | None = Field(default=None)
    end_date: datetime | None = Field(default=None)

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    
class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    is_read: bool

class ContactUpdate(BaseModel):
    is_read: bool | None = Field(default=False)
    
class AboutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    full_name: str 
    headline: str 
    description: str 
    email: EmailStr | None = Field(default=None, alias="email_public")
    profile_image: str | None = Field(default=None, alias="profile_image_link")
    location: str | None = None
    github_link: str
    linkedin_link: str

class AboutUpdate(BaseModel):
    full_name: str | None = Field(default=None)
    headline: str | None = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None, alias="email_public")
    profile_image: str | None = Field(default=None, alias="profile_image_link")
    location: str | None = Field(default=None) 
    github_link: str | None = Field(default=None)
    linkedin_link: str | None = Field(default=None)