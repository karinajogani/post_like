from pydantic import BaseModel

class LikePy(BaseModel):
    """schema of like
    """
    created_by : str
    post_id : str
    # name : str

    class config:
        orm_mode = True
