from pydantic import BaseModel

class LikePy(BaseModel):
    user_id : str
    post_id : str
    # name : str
    
    class config:
        orm_mode = True