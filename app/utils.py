from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
import getpass

class Common:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(String, default=getpass.getuser)
    updated_by = Column(String, default=getpass.getuser)