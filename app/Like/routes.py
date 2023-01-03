from fastapi import APIRouter, Depends
from app.Like.schemas import LikePy
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.Like.models import Like
from app.Post.models import Post


router = APIRouter()

@router.post("/like_post")
def like_post(like : LikePy, db: Session = Depends(get_db)):
    
    new_like = Like(user_id = like.user_id,
                    Post_id = like.Post_id)
    
    post_type = db.query(Post.post_type).filter(Post.id == new_like.Post_id).first()
    public_or_private = post_type["post_type"]
    if public_or_private == "private":
        return "post is private, you can't able to see and like it"
    else:
        db_like = (db.query(Like).filter(Like.user_id == like.user_id,
                                         Like.Post_id == like.Post_id).first())
    
    if db_like is not None:
        return "you already like the post"
    else:
        db.add(new_like)
        
    total_like_column = (db.query(Post.total_like).filter(Post.id == like.Post_id).first())
    
    count = total_like_column["total_like"]
    count = count + 1
    
    db.query(Post).filter(Post.id == like.Post_id).update({"total_like": count})
    
    db.commit()
    # id = new_like.Post_id
    return db.query(Post).filter(Post.id == new_like.Post_id).first()

@router.get("/likes_user_details/{post_id}")
def post_details(Post_id: str, db: Session = Depends(get_db)):
    
    like = db.query(Like).filter(Like.Post_id == Post_id).all()
    
    return like

@router.delete("/dislike")
def dislike_post(like:LikePy, db: Session = Depends(get_db)):
    
    new_like = Like(user_id = like.user_id,
                    Post_id = like.Post_id)
    
    dislike = (db.query(Like).filter(Like.Post_id == new_like.Post_id,
                                     Like.user_id == new_like.user_id).first())
    # db.add(new_like)
    db.delete(dislike)
    db.commit()

    total_like_column = db.query(Post.total_like).filter(Post.id == like.Post_id).first()
    
    count = total_like_column["total_like"]
    count = count - 1
    
    db.query(Post).filter(Post.id == like.Post_id).update({"total_like": count})
    
    db.commit()

    post = db.query(Post).filter(Post.id == like.Post_id).first()
    return {"data": post, "message": "dislike the post"}
