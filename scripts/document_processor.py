import os
import tempfile
import asyncio
from typing import Optional
import aiohttp
import pypandoc
import pandas as pd
from io import BytesIO

class DocumentProcessor:
    """Handle conversion of various document types to markdown."""
    
    def __init__(self):
        # Ensure pandoc is available for document conversion
        try:
            pypandoc.get_pandoc_version()
        except OSError:
            raise RuntimeError("Pandoc is not installed. Please install pandoc first.")
    
    async def download_file(self, url: str) -> Optional[bytes]:
        """Download a file from a URL."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        print(f"Failed to download {url}: Status {response.status}")
                        return None
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            return None
    
    async def convert_pdf_to_markdown(self, content: bytes) -> Optional[str]:
        """Convert PDF content to markdown."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                temp_pdf.write(content)
                temp_pdf.flush()
                
                # Convert PDF to markdown using pandoc
                markdown = pypandoc.convert_file(
                    temp_pdf.name,
                    'markdown',
                    format='pdf',
                    extra_args=['--wrap=none']
                )
                
                os.unlink(temp_pdf.name)
                return markdown
                
        except Exception as e:
            print(f"Error converting PDF to markdown: {str(e)}")
            return None
    
    async def convert_word_to_markdown(self, content: bytes) -> Optional[str]:
        """Convert Word document to markdown."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_doc:
                temp_doc.write(content)
                temp_doc.flush()
                
                # Convert Word to markdown using pandoc
                markdown = pypandoc.convert_file(
                    temp_doc.name,
                    'markdown',
                    format='docx',
                    extra_args=['--wrap=none']
                )
                
                os.unlink(temp_doc.name)
                return markdown
                
        except Exception as e:
            print(f"Error converting Word document to markdown: {str(e)}")
            return None
    
    async def convert_excel_to_markdown(self, content: bytes) -> Optional[str]:
        """Convert Excel file to markdown."""
        try:
            # Read Excel file into pandas
            df = pd.read_excel(BytesIO(content))
            
            # Convert DataFrame to markdown table
            markdown = df.to_markdown(index=False)
            return markdown
            
        except Exception as e:
            print(f"Error converting Excel to markdown: {str(e)}")
            return None
    
    async def convert_csv_to_markdown(self, content: bytes) -> Optional[str]:
        """Convert CSV file to markdown."""
        try:
            # Read CSV file into pandas
            df = pd.read_csv(BytesIO(content))
            
            # Convert DataFrame to markdown table
            markdown = df.to_markdown(index=False)
            return markdown
            
        except Exception as e:
            print(f"Error converting CSV to markdown: {str(e)}")
            return None
    
    async def process_document(self, url: str) -> Optional[str]:
        """Process a document URL and convert it to markdown."""
        # Download the document
        content = await self.download_file(url)
        if not content:
            return None
            
        # Determine file type and convert accordingly
        url_lower = url.lower()
        try:
            if url_lower.endswith('.pdf'):
                return await self.convert_pdf_to_markdown(content)
            elif url_lower.endswith(('.doc', '.docx')):
                return await self.convert_word_to_markdown(content)
            elif url_lower.endswith(('.xls', '.xlsx')):
                return await self.convert_excel_to_markdown(content)
            elif url_lower.endswith('.csv'):
                return await self.convert_csv_to_markdown(content)
            else:
                print(f"Unsupported file type: {url}")
                return None
        except Exception as e:
            print(f"Error processing document {url}: {str(e)}")
            return None
