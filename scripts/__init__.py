"""
Scripts package for webpage and document processing.
"""

from .webpage_to_markdown import main as process_webpage
from .document_processor import DocumentProcessor

__all__ = ['process_webpage', 'DocumentProcessor']
