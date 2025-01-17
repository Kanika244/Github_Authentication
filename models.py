from typing import Optional
from pydantic import BaseModel , EmailStr
from datetime import datetime

class User(BaseModel):
    login: str
    email: Optional[EmailStr]  
    avatar_url: str
    html_url: str
    created_at: datetime
    updated_at: datetime
    token:str


