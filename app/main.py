from fastapi import FastAPI
from .Routers import book, user, book_category
from . import models, database

app = FastAPI()


# For simplicity, we're employing a straightforward migration approach.
# However, for complex database migration handling I will be using alembic
models.Base.metadata.create_all(bind= database.engine)


# rounters registers 
app.include_router(book.router)
app.include_router(user.router)
app.include_router(book_category.router)