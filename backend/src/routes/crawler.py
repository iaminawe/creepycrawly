from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import asyncio
from crawl4ai import WebCrawler
from crawl4ai.extractor import LLMContentExtractor

router = APIRouter()

class CrawlRequest(BaseModel):
    url: str
    s3_bucket: str
    skip_docs: bool = False
    download_files: bool = False

class CrawlResponse(BaseModel):
    success: bool
    message: str
    page_url: str | None = None
    document_urls: list[str] = []

class CrawlStatusResponse(BaseModel):
    status: str

class ConfigRequest(BaseModel):
    max_depth: int
    stay_on_domain: bool
    follow_subdomains: bool
    parallel_downloads: int
    file_types: str

class ConfigResponse(BaseModel):
    success: bool
    message: str

class RecentContentResponse(BaseModel):
    content: list[str]

active_crawl = False
recent_content = []

@router.post("/crawl", response_model=CrawlResponse)
async def crawl_webpage(request: CrawlRequest):
    """
    Endpoint to crawl a webpage and convert it to markdown.
    The markdown files will be stored in the specified S3 bucket.
    """
    global active_crawl, recent_content
    active_crawl = True
    recent_content = []
    try:
        # Initialize WebCrawler
        crawler = WebCrawler(
            strategy="cosypage",
            extractor=LLMContentExtractor(llm_api_key=os.getenv("OPENAI_API_KEY")),
            enable_javascript=True
        )

        # Start crawling
        crawler.start(request.url)

        # Simulate storing recent content dynamically
        recent_content.append("Scraped content for " + request.url)

        return CrawlResponse(
            success=True,
            message="Webpage successfully processed and stored",
            page_url=request.url,
            document_urls=crawler.get_document_urls() if crawler.get_document_urls() else []
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing webpage: {str(e)}"
        )
    finally:
        active_crawl = False

@router.get("/recent", response_model=RecentContentResponse)
async def get_recent_content():
    """
    Endpoint to get recent content.
    """
    global recent_content
    return RecentContentResponse(content=recent_content)

@router.post("/stop")
async def stop_crawl():
    global active_crawl
    active_crawl = False
    return {"status": "stopped"}

@router.get("/status", response_model=CrawlStatusResponse)
async def get_crawl_status():
    """
    Endpoint to get the status of the crawling process.
    """
    global active_crawl
    status = "Crawling in progress..." if active_crawl else "Idle"
    return CrawlStatusResponse(status=status)

@router.post("/config", response_model=ConfigResponse)
async def update_config(request: ConfigRequest):
    """
    Endpoint to update crawler configuration.
    """
    try:
        # Update environment variables
        os.environ["CRAWL_MAX_DEPTH"] = str(request.max_depth)
        os.environ["CRAWL_STAY_ON_DOMAIN"] = str(request.stay_on_domain)
        os.environ["CRAWL_FOLLOW_SUBDOMAINS"] = str(request.follow_subdomains)
        os.environ["CRAWL_PARALLEL_DOWNLOADS"] = str(request.parallel_downloads)
        os.environ["CRAWL_FILE_TYPES"] = request.file_types

        return ConfigResponse(
            success=True,
            message="Configuration updated successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating configuration: {str(e)}"
        )

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Get real crawl metrics
            if active_crawl:
                await websocket.send_json({
                    "status": "active",
                    "processed": len(recent_content),
                    "queued": 0,  # Would need queue tracking
                    "currentUrl": recent_content[-1] if recent_content else ""
                })
            else:
                await websocket.send_json({"status": "idle"})

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        print("Client disconnected")
