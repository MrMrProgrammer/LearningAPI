from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import logging
import sys

from users.router import router as users_router
from books.router import router as books_router
from website.router import router as website_router
from product_scanner.router import router as product_scanner
from economic.router import router as economic_router
from logger.router import router as logger_router
from scraping.router import router as scraping_router

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO, 
    format='%(asctime)s - %(message)s'
)

app = FastAPI(
    docs_url = "/swagger",
    title = "Learning API",
)

app.include_router(economic_router, tags=['Economic'], prefix="/economic")
app.include_router(users_router, tags=['Users'], prefix="/users")
app.include_router(books_router, tags=['Books'], prefix="/books")
app.include_router(product_scanner, tags=['Product Scanner'], prefix="/product_scanner")
app.include_router(logger_router, tags=['Logger'], prefix="/logger")
app.include_router(scraping_router, tags=['Web Scraping'], prefix="/scraping")
app.include_router(website_router, tags=['Website'], prefix="")


app.mount("/static", StaticFiles(directory="website/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
