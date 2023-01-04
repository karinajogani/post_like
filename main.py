import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

"""
This is main file and we have to run this file on uvicorn sever port 8000
"""


if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    uvicorn.run("api:app", host=host, port=int(port), lifespan="on")
