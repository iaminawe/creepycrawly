import os
from pathlib import Path
from typing import Optional, Literal
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class CrawlConfig:
    # Database configuration
    db_type: Literal['sqlite', 'postgres'] = os.getenv('CRAWL_DB_TYPE', 'sqlite')
    db_host: Optional[str] = os.getenv('CRAWL_DB_HOST')
    db_port: Optional[int] = int(os.getenv('CRAWL_DB_PORT', '5432'))
    db_name: str = os.getenv('CRAWL_DB_NAME', 'crawlai.db')
    db_user: Optional[str] = os.getenv('CRAWL_DB_USER')
    db_password: Optional[str] = os.getenv('CRAWL_DB_PASSWORD')

    # Storage configuration
    use_s3_storage: bool = os.getenv('CRAWL_USE_S3', '').lower() == 'true'
    s3_bucket: Optional[str] = os.getenv('CRAWL_S3_BUCKET')
    s3_region: str = os.getenv('CRAWL_S3_REGION', 'us-east-1')
    local_storage_path: str = os.getenv('CRAWL_STORAGE_PATH', './crawl_output')

    # Crawling behavior
    max_depth: int = int(os.getenv('CRAWL_MAX_DEPTH', '3'))
    stay_on_domain: bool = os.getenv('CRAWL_STAY_ON_DOMAIN', 'true').lower() == 'true'
    follow_subdomains: bool = os.getenv('CRAWL_FOLLOW_SUBDOMAINS', 'false').lower() == 'true'
    parallel_downloads: int = int(os.getenv('CRAWL_PARALLEL_DOWNLOADS', '5'))

    # File types to process
    allowed_file_types: list[str] = os.getenv(
        'CRAWL_FILE_TYPES',
        '.pdf,.doc,.docx,.xls,.xlsx,.csv'
    ).split(',')

    # Change detection
    enable_change_detection: bool = os.getenv('CRAWL_CHANGE_DETECTION', 'true').lower() == 'true'
    change_strategy: Literal['content_hash', 'structural'] = os.getenv('CRAWL_CHANGE_STRATEGY', 'structural')
    force_refresh: bool = os.getenv('CRAWL_FORCE_REFRESH', 'false').lower() == 'true'

    @property
    def db_uri(self) -> str:
        """Generate database URI based on configuration"""
        if self.db_type == 'sqlite':
            db_path = Path(self.local_storage_path) / self.db_name
            return f"sqlite:///{db_path}"
        
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def validate(self) -> None:
        """Validate configuration settings"""
        if self.use_s3_storage and not all([self.s3_bucket, self.s3_region]):
            raise ValueError("S3 storage enabled but missing required configuration")

        if self.db_type == 'postgres' and not all([
            self.db_host,
            self.db_port,
            self.db_user,
            self.db_password
        ]):
            raise ValueError("PostgreSQL configuration incomplete")

        # Create local storage directory if it doesn't exist
        if not self.use_s3_storage:
            Path(self.local_storage_path).mkdir(parents=True, exist_ok=True)
            Path(self.local_storage_path, 'website').mkdir(exist_ok=True)
            Path(self.local_storage_path, 'documents').mkdir(exist_ok=True)

    @classmethod
    def from_dict(cls, config_dict: dict) -> 'CrawlConfig':
        """Create configuration from dictionary"""
        return cls(**{
            k: v for k, v in config_dict.items()
            if k in cls.__dataclass_fields__
        })

# Default configuration instance
config = CrawlConfig()
