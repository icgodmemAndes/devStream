import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from .base import db


class MailBlocked(db.Model):
    __tablename__ = 'emails_blocked'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(1000), nullable=False)
    app_uuid = Column(String(200), nullable=False)
    blocked_reason = Column(String(1000), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
