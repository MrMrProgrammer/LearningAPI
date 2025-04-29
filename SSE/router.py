from .schemas import MessageSchema

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from pathlib import Path
from typing import Set
import asyncio

router = APIRouter()

# نگهداری از تمام صف‌های کلاینت
subscribers: Set[asyncio.Queue] = set()

# ------------------------------------------------------------------------

@router.post("/send")
async def send_message(payload: MessageSchema):
    for queue in subscribers:
        await queue.put(payload.message)
    return {"status": "message sent"}

# ------------------------------------------------------------------------

@router.get("/events")
async def sse():
    queue = asyncio.Queue()
    subscribers.add(queue)

    async def event_generator():
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            # کلاینت از اتصال خارج شد، صف رو پاک کن
            subscribers.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ------------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def get_index():
    file_path = Path(__file__).parent / "templates/sse_index.html"
    if not file_path.exists():
        return HTMLResponse(content="File not found", status_code=404)
    html_content = file_path.read_text(encoding="utf-8")
    return HTMLResponse(content=html_content)

# ------------------------------------------------------------------------
