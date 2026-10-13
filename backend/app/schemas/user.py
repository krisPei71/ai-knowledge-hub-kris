from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field

class Token(BaseModel):
    access_token:str
    token_type:str = 'Bearer'

class LoginRequest(BaseModel):
    username:str
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    role:str
    createdAt:datetime = Field(alias="created_at")
    model_config=ConfigDict(from_attributes=True)

