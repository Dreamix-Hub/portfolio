from pydantic import BaseModel, Field, ConfigDict


class AboutBase(BaseModel):
    description: str = Field(min_length=1)
    image_link: str | None = Field(default=None, min_length=1)
    
class AboutResponse(AboutBase):
    pass

class AboutUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=1)
    image_link: str | None = Field(default=None, min_length=1)
    
