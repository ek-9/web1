from fastapi import FastAPI
from week9.router import postRouter, usersRouter

app = FastAPI()
app.include_router(usersRouter.router)
app.include_router(postRouter.router)

@app.get("/")
def main() :
    return {"message": "hello world"}