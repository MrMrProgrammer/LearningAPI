from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    docs_url='/'
)

users_db = {}
books_db = {}

# مدل‌های Pydantic برای کاربر و کتاب
class User(BaseModel):
    id: int
    name: str
    email: str

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int

# API برای مدیریت کاربران
@app.post("/users/", response_model=User)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"detail": "User deleted"}

# API برای مدیریت کتاب‌ها
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    if book.id in books_db:
        raise HTTPException(status_code=400, detail="Book already exists")
    books_db[book.id] = book
    return book

@app.get("/books/", response_model=List[Book])
def get_books():
    return list(books_db.values())

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = books_db.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return {"detail": "Book deleted"}

# برای اجرای اپلیکیشن
# uvicorn main:app --reload