from pydantic import BaseModel

class LikePy(BaseModel):
    user_id : str
    Post_id : str
    # name : str
    
    class config:
        orm_mode = True