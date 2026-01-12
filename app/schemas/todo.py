from pydantic import BaseModel, Field
from typing import Optional


class TodoCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TodoResponse(BaseModel):
    id: int
    title: str
    is_done: bool


class TodoListResponse(BaseModel):
    items: list[TodoResponse]


class TodoUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    is_done: Optional[bool] = None
