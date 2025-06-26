import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.postgres import Base

class BaseModel:
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    @declared_attr
    def created_by_id(cls):
        return Column(Integer, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def updated_by_id(cls):
        return Column(Integer, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def deleted_by_id(cls):
        return Column(Integer, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def created_by(cls):
        return relationship("User", remote_side="[User.id]", foreign_keys=[cls.created_by_id], post_update=True)

    @declared_attr
    def updated_by(cls):
        return relationship("User", remote_side="[User.id]", foreign_keys=[cls.updated_by_id], post_update=True)

    @declared_attr
    def deleted_by(cls):
        return relationship("User", remote_side="[User.id]", foreign_keys=[cls.deleted_by_id], post_update=True)

    def soft_delete(self, deleted_by=None):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        self.deleted_by = deleted_by

    def soft_update(self, updated_by=None):
        self.updated_at = datetime.utcnow()
        self.updated_by = updated_by


class AbstractBaseModel(BaseModel, Base):
    __abstract__ = True
