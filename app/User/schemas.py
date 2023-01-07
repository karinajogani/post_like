from pydantic import BaseModel
from typing import Optional

class UserPy(BaseModel):
    """create schemas for user
    """
    name : str
    email : str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
