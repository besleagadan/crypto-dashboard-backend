from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

class SoftDeleteQuery(Query):
    def not_deleted(self):
        return self.filter_by(is_deleted=False)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    query_cls=SoftDeleteQuery
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
