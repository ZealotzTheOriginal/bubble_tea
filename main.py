from fastapi import FastAPI
from routers import bubbleteas, users

app = FastAPI(title="Bubble Tea & Users API")

app.include_router(bubbleteas.router)
app.include_router(users.router)

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}