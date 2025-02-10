from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .models import Base

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _create_engine(self):
        if self.config.db_type == 'sqlite':
            # SQLite specific configuration
            return create_engine(
                self.config.db_uri,
                connect_args={"check_same_thread": False},
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20
            )
        else:
            # PostgreSQL configuration
            return create_engine(
                self.config.db_uri,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30
            )

    def create_database(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()

    def dispose(self):
        """Close all connections"""
        self.engine.dispose()
