from pydantic import BaseModel

class LikePy(BaseModel):
    created_by : str
    post_id : str
    # name : str

    class config:
        orm_mode = True
