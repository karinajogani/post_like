from fastapi import APIRouter, Depends
from app.Like.schemas import LikePy
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.Like.models import Like
from app.Post.models import Post
from app.User.models import User


router = APIRouter()

@router.post("/like_post")
def like_post(like : LikePy, db: Session = Depends(get_db)):
    
    new_like = Like(user_id = like.user_id,
                    post_id = like.post_id)

    def post_like_function(db, like: LikePy):
        db_like = (db.query(Like).filter(Like.user_id == like.user_id, Like.post_id == like.post_id).first())
        
        if db_like is not None:
            return "You have already like the post"
        else:
            db.add(new_like)
            total_like_column = (db.query(Post.total_like).filter(Post.id == like.post_id).first())
            count = total_like_column["total_like"]
            count = count + 1
            db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})
            db.commit()
            id = new_like.post_id
            return db.query(Post).filter(Post.id == id).first()

    two_post_column = (db.query(Post.post_type, Post.post_display_user).filter(Post.id == new_like.post_id).first())

    public_or_private = two_post_column["post_type"]
    post_user_id_filed = (db.query(Post.user_id).filter(Post.id == new_like.post_id).first())
    post_user_id = post_user_id_filed["user_id"]

    if public_or_private == "public":
        return post_like_function(db, new_like)

    elif public_or_private == "private":
        if new_like.user_id == post_user_id:
            return post_like_function(db, new_like)
        else:
            return "Sorry, This post is private. So you can't see and like it."

    else:
        display_all_users = two_post_column["post_display_user"]
        display_user_list = display_all_users.split()
        if new_like.user_id in display_user_list or new_like.user_id == post_user_id:
            return post_like_function(db, new_like)
        else:
            return "you have no rights to like the post."

@router.get("/like_count/{post_id}")
def count_the_like(post_id: str, db: Session = Depends(get_db)):

    likes = db.query(Like).filter(Like.post_id == post_id).count()
    return likes    

@router.get("/likes_user_details/{post_id}/{user_id}")
def post_details(post_id: str, user_id: str, db: Session = Depends(get_db)):

    post_user_id_column = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user_id = post_user_id_column["user_id"]
    if post_user_id == user_id:
        likes_user_id_filed = (db.query(Like.user_id).filter(Like.post_id == post_id).all())

        like_user_id_list = []
        for i in range(len(likes_user_id_filed)):
            likes_user_id = likes_user_id_filed[i]["user_id"]
            like_user_id_list.append(likes_user_id)

        user_details_list = []
        for j in like_user_id_list:
            user_details = db.query(User).filter(User.id == j).first()
            user_details_list.append(user_details)

        return user_details_list
    else:
        return "Sorry! You can't see the likes user details."

@router.delete("/dislike")
def dislike_post(like:LikePy, db: Session = Depends(get_db)):
    
    new_like = Like(user_id = like.user_id,
                    post_id = like.post_id)
    
    dislike = (db.query(Like).filter(Like.post_id == new_like.post_id,
                                     Like.user_id == new_like.user_id).first())
    # db.add(new_like)
    if dislike is None:
        return "you haven't liked it."
    else:
        db.delete(dislike)
        db.commit()

        total_like_column = db.query(Post.total_like).filter(Post.id == like.post_id).first()
        
        count = total_like_column["total_like"]
        count = count - 1
        
        db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})
        
        db.commit()

        post = db.query(Post).filter(Post.id == like.post_id).first()
        return {"data": post, "message": "dislike the post"}
