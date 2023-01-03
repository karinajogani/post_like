from Database.db_base import Base
from sqlalchemy import Column, ForeignKey
from app.utils import Common
from sqlalchemy.dialects.postgresql import UUID
from app.User.models import User
from app.Post.models import Post

class Like(Common, Base):
    __tablename__ = "Like"
    # name = Column(String)
    user_id = Column(UUID, ForeignKey(User.id))
    post_id = Column(UUID, ForeignKey(Post.id))