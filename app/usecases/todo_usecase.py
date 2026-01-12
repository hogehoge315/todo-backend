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

    def update(self, id: int, title: str | None, is_done: bool | None) -> Todo:
        try:
            """Todoを更新する"""
            # ステップ1: 現在のTodoを取得
            todos = self._repo.list()
            target_todo = next((t for t in todos if t.id == id), None)
            if target_todo is None:
                raise ValueError(f"Todo with id {id} not found")
            # ステップ2: Domain層のメソッドで更新
            updated_todo = target_todo
            if title is not None:
                updated_todo = updated_todo.rename(title)

            if is_done is not None:
                updated_todo = updated_todo.set_done(is_done)
            # ステップ3: リポジトリで保存
            saved = self._repo.update(updated_todo)
            self._db.commit()
            return saved
        except Exception:
            self._db.rollback()
            raise
