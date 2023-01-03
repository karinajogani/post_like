from Database.db_base import Base
from sqlalchemy import Column, String
from app.utils import Common

class User(Common, Base):
    __tablename__ =  "User"
    name = Column(String)
    email = Column(String)

    