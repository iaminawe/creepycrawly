from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ContentVersion(Base):
    __tablename__ = 'content_versions'
    
    id = Column(Integer, primary_key=True)
    url_hash = Column(String(64), index=True)
    url = Column(String(2048))
    content_hash = Column(String(64))
    structural_hash = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)
    crawl_id = Column(Integer, ForeignKey('crawl_history.id'))
    
    # Track content location
    storage_type = Column(String(10))  # 'local' or 's3'
    storage_path = Column(String(1024))
    
    def __repr__(self):
        return f"<ContentVersion(url_hash='{self.url_hash}', created_at='{self.created_at}')>"

class CrawlHistory(Base):
    __tablename__ = 'crawl_history'
    
    id = Column(Integer, primary_key=True)
    start_url = Column(String(2048))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String(50))  # 'running', 'completed', 'failed'
    total_pages = Column(Integer, default=0)
    total_documents = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    
    # Configuration used
    max_depth = Column(Integer)
    stay_on_domain = Column(Boolean)
    storage_type = Column(String(10))
    
    # Relationships
    versions = relationship("ContentVersion", backref="crawl")
    
    def __repr__(self):
        return f"<CrawlHistory(start_url='{self.start_url}', status='{self.status}')>"

class DocumentMetadata(Base):
    __tablename__ = 'document_metadata'
    
    id = Column(Integer, primary_key=True)
    url_hash = Column(String(64), index=True)
    url = Column(String(2048))
    document_type = Column(String(10))  # 'pdf', 'doc', 'xls', etc.
    original_filename = Column(String(512))
    content_hash = Column(String(64))
    extraction_status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    crawl_id = Column(Integer, ForeignKey('crawl_history.id'))
    
    def __repr__(self):
        return f"<DocumentMetadata(url='{self.url}', type='{self.document_type}')>"
