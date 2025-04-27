from .schemas import GetUrl

from fastapi import APIRouter
from newspaper import Article

router = APIRouter()

@router.post("/article/")
async def scrap_article(url: GetUrl):
    """
    Scrape the given URL and return extracted article sections.
    """
    try:
        article = Article(url.url)
        article.download()
        article.parse()

        data = {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": str(article.publish_date) if article.publish_date else None,
            "top_image": article.top_image,
            "images": list(article.images),
            "movies": list(article.movies),
            "source_url": article.source_url,
            "meta_data": article.meta_data,
        }

        return {
            "success": True,
            "result": data
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
