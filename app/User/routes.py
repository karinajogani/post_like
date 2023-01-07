from fastapi import APIRouter, status, Depends, HTTPException
from app.User.schemas import UserPy, UserUpdate
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.User.models import User

router = APIRouter()

@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_new_user(user:UserPy, db:Session = Depends(get_db)):
    """api for create user
    """
    new_user = User(name=user.name,
                    email=user.email)

    db.add(new_user)
    db.commit()
    return{"message" : "user create successfully"}

@router.get("/user", status_code=status.HTTP_200_OK)
def get_user(db:Session = Depends(get_db)):
    """api for get user
    """
    users = db.query(User).all()
    user = [i if(i.is_delete)== False else None for i in users]
    return user

    # for i in users:
    #     if i.is_delete == False:
    #         user.append(i)
    # return user

@router.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_user_by_id(id:str, db: Session = Depends(get_db)):
    """api for get user by id
    """
    user = db.query(User).filter(User.id == id).first()
    # if user.is_delete == True:
    #     return user
    # else:
    #     return {"message" : "this user is deleted"}
    return {"message" : "this user is deleted"} if user.is_delete == True else user

@router.put("/user/{id}", status_code=status.HTTP_200_OK)
def update_user(id:str, user: UserUpdate, db:Session = Depends(get_db)):
    """api for update user
    """
    user_obj = db.query(User).filter(User.id == id).first()

    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if user_obj.is_delete == False:
            data_to_update = user.dict(exclude_unset=True)
            for key, value in data_to_update.items():
                setattr(user_obj, key, value)
            db.commit()
            return {"message" : "user update successfully"}
        return {"message" : "user was deleted"}

@router.delete('/user/{id}')
def delete_user(id: str, db: Session = Depends(get_db)):
    """api for delete user
    """
    delete = db.query(User).filter(User.id == id).first()

    if delete is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else: db.query(User).filter(User.id == id).update({"is_delete":True})

    db.commit()

    return {"message": "User delete successfully"}
