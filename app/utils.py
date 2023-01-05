from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
import getpass
import datetime

class Common:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate =datetime.datetime.utcnow, default=datetime.datetime.utcnow)
    created_by = Column(String, default=getpass.getuser)
    updated_by = Column(String, default=getpass.getuser)
