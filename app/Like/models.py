from Database.db_base import Base
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.User.models import User
from app.Post.models import Post
import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Like(Base):
    """model of post's like
    """
    __tablename__ = "Like"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(UUID, ForeignKey(User.id))
    post_id = Column(UUID, ForeignKey(Post.id))
