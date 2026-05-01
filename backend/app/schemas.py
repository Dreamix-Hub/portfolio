from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AboutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    description: str = Field(min_length=1)
    image_link: str | None = Field(default=None, min_length=1)
    
class AboutUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=1)
    image_link: str | None = Field(default=None, min_length=1)

class TechStackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    languages: str = Field(min_length=1, max_length=100)
    framework: str = Field(min_length=1, max_length=100)
    databases: str = Field(min_length=1, max_length=100)
    tools: str = Field(min_length=1, max_length=100)
    
    
class TechStackUpdate(BaseModel):
    languages: str | None = Field(default=None,min_length=1, max_length=100)
    framework: str | None = Field(default=None,min_length=1, max_length=100)
    databases: str | None = Field(default=None,min_length=1, max_length=100)
    tools: str | None = Field(default=None,min_length=1, max_length=100)   
    
class EducationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    institute: str
    start_date: datetime
    end_date: datetime
