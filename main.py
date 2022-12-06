import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os
from models import Book, Author
from schema import Book as SchemaBook
from schema import Author as SchemaAuthor
from dotenv import load_dotenv
load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/add-author/", response_model=SchemaAuthor)
def add_book(author: SchemaAuthor):
    db_author = Author(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.get("/books/")
def get_books():
    books = db.session.query(Book).all()

    return books

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
