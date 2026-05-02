from pydantic import BaseModel, ConfigDict, EmailStr, Field

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
    
