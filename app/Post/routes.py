from fastapi import APIRouter, status, Depends, HTTPException
from app.Post.schemas import PostPy, PostUpdate
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.Post.models import Post
import datetime

router = APIRouter()

@router.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_new_post(post:PostPy, db:Session = Depends(get_db)):
   
    # breakpoint()
    new_post = Post(title=post.title,
                    description=post.description,
                    user_id=post.user_id,
                    post_type=post.post_type)
    
    db.add(new_post)
    db.commit()
    return{"message" : "post create successfully"}

@router.put("/post/{id}", status_code=status.HTTP_200_OK)
def update_post(id:str, post:PostUpdate, db: Session = Depends(get_db)):
    
    post_obj = db.query(Post).filter(Post.id == id).first()
    
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_obj.updated_at  = datetime.datetime.now()
    
    Data_to_update = post.dict(exclude_unset=True)
    for key, value in Data_to_update.items():
        setattr(post_obj, key, value)
        
    db.commit()
    return {"message" : "post update successfully"}

@router.get("/post", status_code=status.HTTP_404_NOT_FOUND)
def get_all_the_post(db: Session = Depends(get_db)):
   
    post = db.query(Post).all()
    return post

@router.get("/post/{post_id}")
def get_post_and_total_like(post_id: str, db: Session = Depends(get_db)):
  
    post = db.query(Post).filter(Post.id == post_id).first()
    return post

@router.delete('/post/{id}')
def delete_post(id: str, db: Session = Depends(get_db)):

    post_delete = db.query(Post).filter(Post.id == id).first()

    if post_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post_delete)
    db.commit()

    return {"message": "User delete successfully"}