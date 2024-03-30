from fastapi import FastAPI
from .Routers import book, user


app = FastAPI()


# rounters registers 
app.include_router(book.router)
app.include_router(user.router)