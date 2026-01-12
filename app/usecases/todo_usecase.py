from sqlalchemy.orm import Session

from app.domain.todo import Todo
from app.infra.todo_repository_sqlalchemy import SqlAlchemyTodoRepository


class TodoUseCase:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = SqlAlchemyTodoRepository(db)

    def create(self, title: str) -> Todo:
        todo = Todo.new(title=title)
        try:
            created = self._repo.add(todo)
            self._db.commit()
            return created
        except Exception:
            self._db.rollback()
            raise

    def list(self) -> list[Todo]:
        return self._repo.list()
