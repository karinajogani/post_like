import uvicorn


"""
This is main file and we have to run this file on uvicorn sever port 8000
"""


if __name__ == "__main__":

    uvicorn.run("api:app", host="127.0.0.1", port=8000, lifespan="on")