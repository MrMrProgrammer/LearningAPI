from pydantic import BaseModel


class GetUrl(BaseModel):
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.tabnak.ir/fa/news/1301678"
            }
        }