from fastapi import APIRouter
from .schemas import BarcodeData
import jdatetime

router = APIRouter()

database = []

@router.post("/add-barcode/")
def add_barcode(data: BarcodeData):
    timestamp = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "barcode": data.barcode,
        "timestamp": timestamp
    }
    database.append(entry)
    return {"message": "Barcode added", "data": entry}


@router.get("/barcodes/")
def get_barcodes():
    return database
