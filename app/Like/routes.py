from fastapi import APIRouter, Depends, HTTPException, status
from app.Like.schemas import LikePy
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.Like.models import Like
from app.Post.models import Post
from app.User.models import User


router = APIRouter()

@router.post("/like_post")

def like_post(like : LikePy, db: Session = Depends(get_db)):
    """api for post's like
    """
    new_like = Like(created_by = like.created_by,
                    post_id = like.post_id)

    def post_like(db, like: LikePy):
        db_like = (db.query(Like).filter(Like.created_by == like.created_by, Like.post_id == like.post_id).first())
        if db_like is not None: return "You have already like the post"
        else:
            db.add(new_like)
            total_like = (db.query(Post.total_like).filter(Post.id == like.post_id).first())
            count = total_like["total_like"]+1
            db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})
            db.commit()
            return "liked the post"

    post_data = (db.query(Post.post_type, Post.post_display_user).filter(Post.id == new_like.post_id).first())

    public_or_private = post_data["post_type"]
    post_user = (db.query(Post.created_by).filter(Post.id == new_like.post_id).first())
    post_user_id = post_user["created_by"]

    if public_or_private == "public": return post_like(db, new_like)
    else:
        display_users = post_data["post_display_user"].split()
        if new_like.created_by in display_users or new_like.created_by == post_user_id: return post_like(db, new_like)
        else: return "you have no rights to like the post."

@router.get("/like_count/{post_id}")
def count_the_like(post_id: str, db: Session = Depends(get_db)):
    """api for get post's like count
    """
    likes = db.query(Like).filter(Like.post_id == post_id).count()
    return likes

@router.get("/likes_user_details/{post_id}/{created_by}")
def like_details(post_id: str, created_by: str, db: Session = Depends(get_db)):
    """api for get likes user detail
    """
    post_data = db.query(Post.created_by, Post.is_delete).filter(Post.id == post_id).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if post_data.is_delete == False:
            post_user_id = post_data["created_by"]
            if post_user_id == created_by:
                like_by = (db.query(Like.created_by).filter(Like.post_id == post_id).all())
                like_data = [like_by[i]["created_by"] for i in range(len(like_by))]
                user_data = [db.query(User).filter(User.id == i).first() for i in like_data]
                return user_data
            else: return "Sorry! You can't see the likes user details."
        else: return {"message" : "user was deleted"}

@router.delete("/dislike")
def dislike_post(like:LikePy, db: Session = Depends(get_db)):
    """api for dislike
    """

    new_like = Like(created_by = like.created_by,
                    post_id = like.post_id)

    dislike = (db.query(Like).filter(Like.post_id == new_like.post_id,
                                     Like.created_by == new_like.created_by).first())
    if dislike is None: return "you haven't liked it."
    else:
        db.delete(dislike)

        total_like = db.query(Post.total_like).filter(Post.id == like.post_id).first()
        count = total_like["total_like"]-1
        db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})

        db.commit()
        return "dislike the post"
