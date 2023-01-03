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
                    post_type=post.post_type,
                    post_display_user=post.post_display_user)

    db.add(new_post)
    db.commit()
    return{"message" : "post create successfully"}

@router.put("/post/{id}", status_code=status.HTTP_200_OK)
def update_post(post_id:str, user_id:str, post:PostUpdate, db: Session = Depends(get_db)):

    post_obj = db.query(Post).filter(Post.id == id).first()
    post_user_id = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user = post_user_id["user_id"]
    if post_user== user_id:

        post_obj.updated_at = datetime.now()
        post_dict = post.dict(exclude_unset=True)

        for key, value in post_dict.items():
            setattr(post_obj, key, value)

        db.commit()
        return {"message": "Post updated successfully"}
    else:
        return "You have no rights for update"

    # if not post_obj:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # post_obj.updated_at  = datetime.datetime.now()

    # Data_to_update = post.dict(exclude_unset=True)
    # for key, value in Data_to_update.items():
    #     setattr(post_obj, key, value)

    # db.commit()
    # return {"message" : "post update successfully"}

@router.get("/post", status_code=status.HTTP_404_NOT_FOUND)
def get_all_the_post(db: Session = Depends(get_db)):

    post = db.query(Post).all()
    return post

@router.get("/post/{post_id}")
def get_post_and_total_like(post_id: str, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()
    return post

@router.get("/post/{post_id}/{user_id}")
def post_and_total_like(post_id: str, user_id: str, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()
    # return post

    two_post = (db.query(Post.post_type, Post.post_display_user).filter(Post.id == post_id).first())
    public_or_private = two_post["post_type"]
    post_user_id_filed = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user_id = post_user_id_filed["user_id"]

    if public_or_private == "public":
        return post

    elif public_or_private == "private":
        if user_id == post_user_id:
            return post
        else:
            return "Sorry, This post is private. So you can't see it."

    else:
        display_all_users = two_post["post_display_user"]
        display_user_list = display_all_users.split()
        if user_id in display_user_list or user_id == post_user_id:
            return post
        else:
            return "Sorry, This post is private. So you can't see it."

@router.delete('/post/{id}')
def delete_post(id: str, db: Session = Depends(get_db)):

    post_delete = db.query(Post).filter(Post.id == id).first()

    if post_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post_delete)
    db.commit()

    return {"message": "User delete successfully"}
