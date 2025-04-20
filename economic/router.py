from datetime import datetime, timedelta
from fastapi import APIRouter
import requests

router = APIRouter()

# حافظه‌ی کش برای قیمت دلار
dollar_cache = {
    "price": None,
    "expiration": None
}

def fetch_dollar_price():
    url = "https://call1.tgju.org/ajax.json"

    for attempt in range(5):
        try:
            response = requests.get(url, timeout=1)
            response.raise_for_status()  # چک کن خطای HTTP نداشته باشه

            data = response.json()

            price_str = data.get('current', {}).get('price_dollar_rl', {}).get('p')

            if price_str:
                price = int(price_str.replace(",", ""))
                return price

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"[Attempt {attempt+1}] Error fetching dollar price: {e}")
            continue

    return None  # فقط اگر همه تلاش‌ها شکست خورد

@router.get("/dollar")
def get_dollar_price():
    now = datetime.now()

    if dollar_cache["price"] is not None and dollar_cache["expiration"] is not None:
        if dollar_cache["expiration"] > now:
            return {
                "success": True,
                "price": dollar_cache["price"]
            }

    # یا کش منقضی شده یا پرایس نداریم، پس Fetch کنیم
    price = fetch_dollar_price()

    if price is not None:
        dollar_cache["price"] = price
        dollar_cache["expiration"] = now + timedelta(minutes=5)
        return {
            "success": True,
            "price": price
        }
    else:
        return {
            "success": False,
            "price": None
        }
