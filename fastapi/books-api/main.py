from fastapi import FastAPI, HTTPException
from .schemas import BookAuthorPayload, Book, Author
from . import database
app = FastAPI()


@app.get("/")
def get_root():
    return "Welcom to the books api"


@app.get("/book/{book_id}")
def get_book(book_id: int):
    res = database.get_book(book_id)
    if not res:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return res


@app.post("/book/")
def create_book(request: BookAuthorPayload):
    database.add_book(convert_into_book_db_model(request.book),
                      convert_into_author_db_model(request.author))
    return f"New Book Added! \nBook: {request.book.title}\nTotal Pages: {request.book.number_of_pages}\nAuthor: {request.author.first_name} {request.author.last_name}"


def convert_into_book_db_model(book: Book):
    return database.Book(title=book.title, number_of_pages=book.number_of_pages)


def convert_into_author_db_model(author: Author):
    return database.Author(first_name=author.first_name, last_name=author.last_name)
