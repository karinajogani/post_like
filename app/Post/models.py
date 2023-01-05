from Database.db_base import Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.User.models import User
from app.utils import Common

class Post(Common, Base):
    __tablename__ = "Post"
    title = Column(String)
    description = Column(String)
    created_by = Column(UUID, ForeignKey(User.id))
    total_like = Column(Integer, default=0)
    post_type = Column(String)
    post_display_user = Column(String)
