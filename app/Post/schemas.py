from pydantic import BaseModel
from typing import Optional

class PostPy(BaseModel):
    title : str
    description : str
    user_id : str
    post_type : str
    
    # class config:
    #     orm_mode = True
        

class PostUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    post_display_user: Optional[str] = None