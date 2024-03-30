from fastapi import FastApi, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from typing import List, Optional

from .. import sechemaes, models, database

router = APIRouter(
    prefix="/books", 
    tags=["Book"]
)


@router.get("/list", response_model=List[sechemaes.BookGet])
def books(db: Session = Depends(database.get_db) 
          , limit: int = 10
          , skip: int = 0
          , category_id: Optional[int] = None
          , owners_ids: Optional[List[int]] = None):
    query = db.query(models.Book) \
        .join(models.BookCategory, models.Book.category_id == models.BookCategory.id, isouter = True) \
        .group_by(models.Book.id)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    if owner_id is not None:
        query = query.filter(models.Book.owner_id.in_(owners_ids))
    
    return query \
        .limit(limit) \
        .offset(skip) \
        .all() 
        
        
@router("/get", response_model = sechemaes.BookGet)
def book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(id == book_id).first()
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="book doesn't exists")
    
    return book

