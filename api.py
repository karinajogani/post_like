from fastapi import FastAPI
from app.User.routes import router as Userrouter
from app.Post.routes import router as Postrouter
from app.Like.routes import router as Likerouter

app = FastAPI()

app.get("/")
def homepage():
    return {"data" : "you are at the homepage"}

app.include_router(Userrouter, tags=["User"])
app.include_router(Postrouter, tags=["Post"])
app.include_router(Likerouter, tags=["Like"])
