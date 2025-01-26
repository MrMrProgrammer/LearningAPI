from fastapi.responses import HTMLResponse
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/")
def home():

    with open("website/templates/index.html", "r", encoding='utf-8') as f:
        content = f.read()

    return HTMLResponse(content=content, status_code=status.HTTP_200_OK)
