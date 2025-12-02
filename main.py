from fastapi import FastAPI
from router import users, post

app = FastAPI()
app.include_router(users.router)
app.include_router(post.router)

@app.get("/")
def main() :
    return {"message": "hello world"}