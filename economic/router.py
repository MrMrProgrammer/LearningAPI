from datetime import datetime, timedelta
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
import requests
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

# ================================================================
# Cache

# حافظه‌ی کش برای قیمت‌ها
prices_cache = {
    "expiration": None,
    "gold": None,
    "dollar": None,
    "full_coin": None,
    "quarter_coin": None,
    "half_coin": None,
    "tether": None
}

# ================================================================
# Mapping keys for prices
TGJU_KEYS = {
    "dollar": "price_dollar_rl",         # قیمت دلار
    "gold": "geram18",                   # قیمت طلا
    "full_coin": "sekeb",                # قیمت سکه تمام بهار آزادی
    "quarter_coin": "rob",               # قیمت ربع سکه
    "half_coin": "nim",                  # قیمت نیم سکه
    "tether": "crypto-tether-irr",       # قیمت تتر
}

# ================================================================
# Logic

def fetch_price_from_api(price_key):
    """ برای گرفتن قیمت یک ارز خاص از API """
    url = "https://call1.tgju.org/ajax.json"

    for attempt in range(5):
        try:
            response = requests.get(url, timeout=1)
            response.raise_for_status()

            data = response.json()

            print(f"Response data: {data}")  # برای دیباگ

            current = data.get('current', {})
            if not current:
                continue

            price_str = current.get(price_key, {}).get('p')

            if price_str:
                return try_parse_price(price_str)
            return None  # اگر قیمت نباشه

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"[Attempt {attempt+1}] Error fetching price: {e}")
            continue

    return None  # فقط اگر همه تلاش‌ها شکست خورد

def try_parse_price(price_str):
    """ برای تبدیل رشته قیمت به عدد """
    if not price_str:
        return None
    try:
        return int(price_str.replace(",", ""))
    except Exception:
        return None

def fetch_all_prices():
    """ برای گرفتن همه قیمت‌ها """
    prices = {}
    for key, api_key in TGJU_KEYS.items():
        price = fetch_price_from_api(api_key)
        prices[key] = price
    return prices

# ================================================================
# Response Model

class PriceResponse(BaseModel):
    success: bool
    price: Optional[int]

class PricesResponse(BaseModel):
    success: bool
    prices: Optional[dict]

# ================================================================
# Rate Limiter

limiter = Limiter(key_func=get_remote_address)

# ================================================================
# Endpoint

@router.get("/prices", response_model=PricesResponse)
@limiter.limit("20/minute")  # محدود کردن به 20 درخواست در دقیقه
async def get_all_prices(request: Request):  # اضافه کردن پارامتر request
    now = datetime.now()

    # چک کردن کش
    if prices_cache["expiration"] is not None and prices_cache["expiration"] > now:
        # کش معتبره
        return PricesResponse(success=True, prices={key: prices_cache[key] for key in prices_cache if key != "expiration"})

    # کش منقضی شده، باید اطلاعات جدید رو بگیریم
    fetched_prices = fetch_all_prices()

    if fetched_prices:
        # ذخیره‌ی قیمت‌ها در کش
        prices_cache.update(fetched_prices)
        prices_cache["expiration"] = now + timedelta(minutes=5)

        return PricesResponse(success=True, prices=fetched_prices)
    else:
        return PricesResponse(success=False, prices=None)

# ================================================================
# Endpoint for dollar (use cache here too)

@router.get("/dollar", response_model=PriceResponse)
@limiter.limit("20/minute")  # محدود کردن به 20 درخواست در دقیقه
async def get_dollar_price(request: Request):  # اضافه کردن پارامتر request
    now = datetime.now()

    if prices_cache["dollar"] is not None and prices_cache["expiration"] is not None:
        if prices_cache["expiration"] > now:
            return PriceResponse(success=True, price=prices_cache["dollar"])

    # کش منقضی شده یا قیمت نداریم
    price = fetch_price_from_api(TGJU_KEYS["dollar"])

    if price is not None:
        prices_cache["dollar"] = price
        prices_cache["expiration"] = now + timedelta(minutes=5)
        return PriceResponse(success=True, price=price)
    else:
        return PriceResponse(success=False, price=None)
