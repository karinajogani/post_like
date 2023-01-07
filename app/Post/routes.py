from fastapi import APIRouter, status, Depends, HTTPException
from app.Post.schemas import PostPy, PostUpdate
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.Post.models import Post

router = APIRouter()

@router.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_new_post(post:PostPy, db:Session = Depends(get_db)):
    """api for create post
    """
    new_post = Post(title=post.title,
                    description=post.description,
                    created_by=post.created_by,
                    post_type=post.post_type,
                    post_display_user=post.post_display_user)

    db.add(new_post)
    db.commit()
    return{"message" : "post create successfully"}

@router.put("/post/{id}", status_code=status.HTTP_200_OK)
def update_post(id:str, created_by:str, post:PostUpdate, db: Session = Depends(get_db)):
    """api for post update
    """
    post_obj = db.query(Post).filter(Post.id == id).first()
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if post_obj.is_delete == False:
            post_user_id = db.query(Post.created_by).filter(Post.id == id).first()
            post_user = post_user_id["created_by"]
            if post_user== created_by:
                post_dict = post.dict(exclude_unset=True)
                for key, value in post_dict.items():
                    setattr(post_obj, key, value)
                db.commit()
                return {"message": "Post updated successfully"}
            else: return {"You have no rights for update"}
        else: return {"message" : "user was deleted"}

    # if not post_obj:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # post_obj.updated_at  = datetime.datetime.now()

    # Data_to_update = post.dict(exclude_unset=True)
    # for key, value in Data_to_update.items():
    #     setattr(post_obj, key, value)

    # db.commit()
    # return {"message" : "post update successfully"}

@router.get("/post", status_code=status.HTTP_200_OK)
def get_all_the_post(db: Session = Depends(get_db)):
    """api for get all post
    """
    posts = db.query(Post).all()
    post = [i if(i.is_delete)==False else None for i in posts]
    return post

@router.get("/post/{post_id}/{created_by}")
def post_and_total_like(post_id: str, created_by: str, db: Session = Depends(get_db)):
    """api for get post and their like by id
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    # return post
    if post.is_delete == False:
        two_post = (db.query(Post.post_type, Post.post_display_user).filter(Post.id == post_id).first())
        public_or_private = two_post["post_type"]
        id_data = db.query(Post.created_by).filter(Post.id == post_id).first()
        post_user_id = id_data["created_by"]
        if public_or_private == "public": return post
        else:
            user_data = two_post["post_display_user"].split()
            return "Sorry, This post is private. So you can't see it."if created_by in user_data or created_by == post_user_id else post
    else: return {"message" : "user was deleted"}

@router.delete('/post/{id}')
def delete_post(id: str, db: Session = Depends(get_db)):
    """api for delete post
    """
    delete = db.query(Post).filter(Post.id == id).first()

    if delete is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    else: db.query(Post).filter(Post.id == id).update({"is_delete":True})

    db.commit()
    return {"message": "User delete successfully"}
