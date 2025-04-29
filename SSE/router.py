from .schemas import MessageSchema

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from pathlib import Path
import asyncio

router = APIRouter()

message_queue = asyncio.Queue()


@router.post("/send")
async def send_message(payload: MessageSchema):
    await message_queue.put(payload.message)
    return {"status": "message sent"}

# ------------------------------------------------------------------------

@router.get("/events")
async def sse():
    async def event_generator():
        while True:
            message = await message_queue.get()
            yield f"data: {message}\n\n"

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
