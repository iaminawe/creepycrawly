from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from src.webpage_to_markdown import process_webpage

router = APIRouter()

class CrawlRequest(BaseModel):
    url: str
    s3_bucket: str
    skip_docs: bool = False

class CrawlResponse(BaseModel):
    success: bool
    message: str
    page_url: str | None = None
    document_urls: list[str] = []

@router.post("/crawl", response_model=CrawlResponse)
async def crawl_webpage(request: CrawlRequest):
    """
    Endpoint to crawl a webpage and convert it to markdown.
    The markdown files will be stored in the specified S3 bucket.
    """
    try:
        # Process the webpage and get document URLs
        document_urls = await process_webpage(request.url, request.s3_bucket)
        
        return CrawlResponse(
            success=True,
            message="Webpage successfully processed and stored",
            page_url=request.url,
            document_urls=document_urls if document_urls else []
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing webpage: {str(e)}"
        )
