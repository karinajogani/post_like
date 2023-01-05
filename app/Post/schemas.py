from pydantic import BaseModel
from typing import Optional

class PostPy(BaseModel):
    title : str
    description : str
    created_by : str
    post_type : str
    post_display_user: str

    class config:
        orm_mode = True


class PostUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    post_display_user: Optional[str] = None
