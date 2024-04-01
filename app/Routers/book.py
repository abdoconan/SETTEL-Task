from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Query

from sqlalchemy.orm import Session, joinedload

from typing import List, Optional

from .. import sechemaes, models, database, oauth2

router = APIRouter(
    prefix="/books", 
    tags=["Book"]
)

def validate_book_category(category_id: int, db: Session) -> bool:
    if db.query(models.BookCategory).filter(models.BookCategory.id == category_id).first() is None:
        return False
    return True

def get_book_by_id(book_id: int, db: Session) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id) \
        .options(joinedload(models.Book.category), joinedload(models.Book.owner)) \
        .first()

@router.get("/list", response_model=List[sechemaes.BookGet])
def books(db: Session = Depends(database.get_db) 
          , limit: int = Query(10, ge=1, le=100)
          , skip: int = Query(0, ge=0)
          , category_id: Optional[int] = Query(None, ge=1)
          , owners_ids: Optional[List[int]] = Query(None)):
    query = db.query(models.Book) \
        .options(joinedload(models.Book.category), joinedload(models.Book.owner)) 
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    if owners_ids is not None:
        query = query.filter(models.Book.owner_id.in_(owners_ids))
    
    return query \
        .limit(limit) \
        .offset(skip) \
        .all() 
        
        
@router.get("/get", response_model=sechemaes.BookGet)
def single_book(book_id: int, db: Session = Depends(database.get_db)):
    book = get_book_by_id(book_id, db)
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="book doesn't exists")
    
    return book


@router.post("/new", response_model=sechemaes.BookGet, status_code= status.HTTP_201_CREATED)
def create_book(book : sechemaes.BookBase
                , db: Session = Depends(database.get_db)
                , current_user: models.User = Depends(oauth2.get_current_user)):
    book_category_exists =  validate_book_category(book.category_id, db)
    if not book_category_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="book category doesn't exists")
    new_book = models.Book(**book.dict())
    new_book.owner_id = current_user.id
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return db.query(models.Book) \
        .filter(models.Book.id == new_book.id) \
        .options(joinedload(models.Book.category), joinedload(models.Book.owner)) \
        .first()
        
        
@router.put("/edit", response_model=sechemaes.BookGet, status_code= status.HTTP_200_OK)
def edit_book(book_to_update : sechemaes.BookUpdate
                , db: Session = Depends(database.get_db)
                , current_user: models.User = Depends(oauth2.get_current_user)):

    book = get_book_by_id(book_to_update.id, db)
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="book doesn't exists")
    if book.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="you can't edit this book")
    book_category_exists =  validate_book_category(book_to_update.category_id, db)
    if not book_category_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="book category doesn't exists")
    book.title = book_to_update.title
    book.brief = book_to_update.brief
    book.category_id = book_to_update.category_id
    db.commit()
    return db.query(models.Book) \
        .filter(models.Book.id == book.id) \
        .options(joinedload(models.Book.category), joinedload(models.Book.owner)) \
        .first()