from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# region: User 

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True,  nullable=False)
    email = Column(String(512), unique=True, nullable=False)
    user_name = Column(String(512), unique=True, nullable=False)
    password = Column(String(512))
    current_token = Column(String, nullable=True)
    last_action_time = Column(TIMESTAMP(timezone= True), nullable=True)
    created_at = Column(TIMESTAMP(timezone= True), nullable=False, server_default= text('CURRENT_TIMESTAMP'))

# endregion


# region: Book

class BookCategory(Base):
    __tablename__ = 'book_categories'
    
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String(512), unique=True, nullable=False)
    

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True,  nullable=False)
    title = Column(String(255), nullable=False)
    preif = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone= True), nullable=False, server_default= text('CURRENT_TIMESTAMP'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("book_categories.id", ondelete="CASCADE"), nullable=False)
    
    owner =  relationship("User")
    category - relationship("BookCategory")

# endregion
