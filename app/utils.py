from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

class Common:
    """Created common field for models
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate =datetime.datetime.utcnow, default=datetime.datetime.utcnow)
    is_delete = Column(Boolean, default=False)
