import os
import asyncio
import boto3
from typing import List, Optional
from urllib.parse import urlparse, urljoin
import re
from crawl4ai.async_webcrawler import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig, BrowserConfig
from crawl4ai.models import CrawlResult
from src.document_processor import DocumentProcessor

# S3 client setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

def url_to_key(url: str) -> str:
    """Convert URL to a valid S3 key."""
    parsed = urlparse(url)
    # Create a key based on domain and path
    key = f"{parsed.netloc}{parsed.path}"
    if not key.endswith('/'):
        key += '/'
    # Remove invalid characters and replace with underscores
    key = re.sub(r'[^a-zA-Z0-9/.-]', '_', key)
    return key.strip('/')

async def upload_to_s3(bucket: str, key: str, content: str) -> bool:
    """Upload content to S3 bucket."""
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=content.encode('utf-8'),
            ContentType='text/markdown'
        )
        return True
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False

def extract_document_urls(base_url: str, links: dict) -> List[str]:
    """Extract URLs of documents from crawl results."""
    document_extensions = ('.pdf', '.xls', '.xlsx', '.csv', '.doc', '.docx')
    document_urls = []
    
    # Check both internal and external links
    for link_type in ['internal', 'external']:
        if link_type in links:
            for link in links[link_type]:
                if 'href' in link and any(link['href'].lower().endswith(ext) for ext in document_extensions):
                    # Convert relative URLs to absolute URLs
                    url = link['href']
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(base_url, url)
                    document_urls.append(url)
    
    return document_urls

async def process_webpage(url: str, s3_bucket: str) -> Optional[List[str]]:
    """Process a webpage and store its markdown in S3."""
    try:
        # Configure browser settings
        browser_config = BrowserConfig(
            browser_type="chromium",
            headless=True
        )
        
        # Configure crawler settings
        crawler_config = CrawlerRunConfig(
            download_files=True,
            file_extensions=['.pdf', '.xls', '.xlsx', '.csv', '.doc', '.docx']
        )
        
        # Initialize and run crawler
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result: CrawlResult = await crawler.arun(
                url=url,
                config=crawler_config
            )
            
            if result.success:
                # Get markdown content
                markdown_content = result.markdown
                if isinstance(markdown_content, str):
                    # Upload markdown to S3
                    markdown_key = f"pages/{url_to_key(url)}.md"
                    success = await upload_to_s3(s3_bucket, markdown_key, markdown_content)
                    
                    if success:
                        print(f"Successfully uploaded markdown for {url}")
                        # Extract and return document URLs
                        return extract_document_urls(url, result.links)
                    else:
                        print(f"Failed to upload markdown for {url}")
                else:
                    print(f"No markdown content generated for {url}")
            else:
                print(f"Failed to crawl {url}: {result.error_message}")
                
    except Exception as e:
        print(f"Error processing webpage {url}: {str(e)}")
    
    return None

async def process_documents(document_urls: List[str], s3_bucket: str):
    """Process document URLs and convert them to markdown."""
    try:
        processor = DocumentProcessor()
        
        for url in document_urls:
            print(f"Processing document: {url}")
            
            # Convert document to markdown
            markdown_content = await processor.process_document(url)
            
            if markdown_content:
                # Generate S3 key for the document
                doc_key = f"documents/{url_to_key(url)}.md"
                
                # Upload to S3
                success = await upload_to_s3(s3_bucket, doc_key, markdown_content)
                
                if success:
                    print(f"Successfully converted and uploaded {url}")
                else:
                    print(f"Failed to upload converted document {url}")
            else:
                print(f"Failed to convert document {url}")
                
    except Exception as e:
        print(f"Error in document processing: {str(e)}")

async def main(url: str, s3_bucket: str):
    """Main function to orchestrate the webpage and document processing."""
    # Process the webpage and get document URLs
    document_urls = await process_webpage(url, s3_bucket)
    
    if document_urls:
        print(f"Found {len(document_urls)} documents to process")
        # Process the found documents
        await process_documents(document_urls, s3_bucket)
    else:
        print("No documents found or webpage processing failed")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert webpage and its documents to markdown')
    parser.add_argument('url', help='URL of the webpage to process')
    parser.add_argument('s3_bucket', help='S3 bucket to store the markdown files')
    parser.add_argument('--skip-docs', action='store_true', help='Skip processing of linked documents')
    
    args = parser.parse_args()
    
    asyncio.run(main(args.url, args.s3_bucket))
