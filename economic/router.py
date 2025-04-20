from fastapi import APIRouter
from bs4 import BeautifulSoup
import requests

router = APIRouter()

@router.get("/dollar")
def dollar():

    url = "https://www.tgju.org/profile/price_dollar_rl"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dollar_price = soup.find("span", attrs={"data-col": "info.last_trade.PDrCotVal"}).text
    dollar_price = int(dollar_price.replace(",", ""))

    return {
        "success": True,
        "price" : dollar_price
    }
