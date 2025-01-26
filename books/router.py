from fastapi import HTTPException, APIRouter
from .schemas import Book
from typing import List


router = APIRouter()


books_db = {}


@router.post("/", response_model=Book)
def create_book(book: Book):
    if book.id in books_db:
        raise HTTPException(status_code=400, detail="Book already exists")
    books_db[book.id] = book
    return book


@router.get("/", response_model=List[Book])
def get_books():
    return list(books_db.values())


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = books_db.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return {"detail": "Book deleted"}

