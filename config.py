from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from users.router import router as users_router
from books.router import router as books_router

app = FastAPI(
    docs_url = "/swagger",
    title = "Learning API",
)

app.include_router(users_router, tags=['Users'], prefix="/users")
app.include_router(books_router, tags=['Books'], prefix="/books")

app.mount("/static", StaticFiles(directory="website/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
