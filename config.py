from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from users.router import router as users_router
from books.router import router as books_router
from website.router import router as website_router
from product_scanner.router import router as product_scanner
from chain_store.router import router as chain_store

app = FastAPI(
    docs_url = "/swagger",
    title = "Learning API",
)

app.include_router(users_router, tags=['Users'], prefix="/users")
app.include_router(books_router, tags=['Books'], prefix="/books")
app.include_router(product_scanner, tags=['Product Scanner'], prefix="/product_scanner")
app.include_router(chain_store, tags=['Chain Store'], prefix="/chain_store")
app.include_router(website_router, tags=['Website'], prefix="")

app.mount("/static", StaticFiles(directory="website/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
