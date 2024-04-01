from pydantic import BaseModel, EmailStr
from datetime import datetime

from typing import Optional

from .utils import get_current_datetime


# region: Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        from_attributes = True
# endregion

# region: User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreate(UserBase):
    password : str
    
class UserGet(UserBase):
    id: int

# endregion

# region: Book Category
class BookCategoryBase(BaseModel):
    description: str
    
    class Config:
        from_attributes = True

class BookCategoryGet(BookCategoryBase):
    id : int
    
    class Config:
        from_attributes = True
        
    
# endregion


# region: Book

class BookBase(BaseModel):
    title: str
    brief: str
    created_at: datetime = get_current_datetime
    category_id : int
    
    class Config:
        from_attributes = True
    
class BookUpdate(BookBase):
    id: int

class BookGet(BookUpdate):
    owner_id : int 
    category: BookCategoryGet
    owner: UserGet
    
    class Config:
        from_attributes = True

# endregion