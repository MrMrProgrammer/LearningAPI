from fastapi import APIRouter, Request
from datetime import datetime
import logging

router = APIRouter()

# تنظیم لاگر برای ذخیره در فایل
logging.basicConfig(filename="logs.txt", level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("redirect-logger")

@router.post("/log-visit")
async def log_visit(request: Request):
    # IP کلاینت
    client_host = request.client.host

    # هدرهای مرورگر
    headers = dict(request.headers)

    # user-agent و referrer
    user_agent = headers.get("user-agent", "unknown")
    referer = headers.get("referer", "unknown")

    # زمان لاگ
    timestamp = datetime.utcnow().isoformat()

    # بادی درخواست (در صورت وجود)
    try:
        body = await request.json()
    except:
        body = {}

    # لاگ‌کردن اطلاعات
    log_message = f"""
    🚀 Visit Logged:
    IP: {client_host}
    Time: {timestamp}
    User-Agent: {user_agent}
    Referer: {referer}
    Body: {body}
    """
    logger.info(log_message)

    return {"status": "ok", "message": "visit logged"}
