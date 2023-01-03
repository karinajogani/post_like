from fastapi import APIRouter, status, Depends, HTTPException
from app.User.schemas import UserPy, UserUpdate
from sqlalchemy.orm import Session
from Database.db_base import get_db
from app.User.models import User
import datetime

router = APIRouter()

@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_new_user(user:UserPy, db:Session = Depends(get_db)):
    
    new_user = User(name=user.name,
                    email=user.email)
    
    new_user.created_at = datetime.datetime.now()
    
    db.add(new_user)
    db.commit()
    return{"message" : "user create successfully"}

@router.get("/user", status_code=status.HTTP_200_OK)
def get_user(db:Session = Depends(get_db)):
    
    users = db.query(User).all()
    return users

@router.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_user_by_id(id:str, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == id).first()
    return user

@router.put("/user/{id}", status_code=status.HTTP_200_OK)
def update_user(id:str, user: UserUpdate, db:Session = Depends(get_db)):
    
    user_obj = db.query(User).filter(User.id == id).first()
    
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    user_obj.updated_at = datetime.datetime.now()
    
    data_to_update = user.dict(exclude_unset=True)
    for key, value in data_to_update.items():
        setattr(user_obj, key, value)

    db.commit()
    return {"message" : "user update successfully"}

@router.delete('/user/{id}')
def delete_user(id: str, db: Session = Depends(get_db)):

    user_delete = db.query(User).filter(User.id == id).first()

    if user_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user_delete)
    db.commit()

    return {"message": "User delete successfully"}