from fastapi import FastAPI

from app.database import engine
from app.models.todo import Base
from app.routers.todos import router as todo_router

app = FastAPI()

app.include_router(todo_router)

Base.metadata.create_all(bind=engine)
