from sqlalchemy import Column, Integer, String, Boolean
from app.db.postgres import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    provider = Column(String)
    provider_id = Column(String, unique=True)

    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
