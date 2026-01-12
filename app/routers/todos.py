from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.todo import TodoCreateRequest, TodoListResponse, TodoResponse
from app.usecases.todo_usecase import TodoUseCase

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(req: TodoCreateRequest, db: Session = Depends(get_db)) -> TodoResponse:
    uc = TodoUseCase(db)
    try:
        todo = uc.create(title=req.title)
        return TodoResponse(id=todo.id, title=todo.title, is_done=todo.is_done)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=TodoListResponse)
def list_todos(db: Session = Depends(get_db)) -> TodoListResponse:
    uc = TodoUseCase(db)
    todos = uc.list()
    return TodoListResponse(
        items=[TodoResponse(id=t.id, title=t.title, is_done=t.is_done) for t in todos]
    )
