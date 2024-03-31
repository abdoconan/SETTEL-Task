from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Query

from sqlalchemy.orm import Session

from typing import List, Optional

from .. import sechemaes, models, database

router = APIRouter(
    prefix="/book_categories", 
    tags=["Book Category"]
)


@router.get("/list", response_model=List[sechemaes.BookCategoryGet])
def book_categories(db: Session = Depends(database.get_db)):
    return db.query(models.BookCategory).all()


@router.post("/create", response_model=sechemaes.BookCategoryGet)
def book_category_create(new_book: sechemaes.BookCategoryBase, db: Session = Depends(database.get_db)):
    new_book = models.BookCategory(**new_book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book