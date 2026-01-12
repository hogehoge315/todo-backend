# infraでは、Protocolで定義されたリポジトリの実装を行う
# SQLAlchemyを使って、データベースとのやり取りを実装します。
# 実際のデータベース操作はSQLAlchemyのセッションを通じて行います。

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.todo import Todo
from app.models.todo import TodoModel
from app.repositories.todo_repository import TodoRepository


class SqlAlchemyTodoRepository(
    TodoRepository
):  # Protocolで定義されたインターフェースを実装
    def __init__(
        self, db: Session
    ) -> None:  # コンストラクタでSQLAlchemyのセッションを受け取る
        self._db = db  # セッションをインスタンス変数に保存

    def add(self, todo: Todo) -> Todo:  # Todoを追加するメソッドの実装
        row = TodoModel(
            title=todo.title, is_done=todo.is_done
        )  # TodoModelのインスタンスを作成
        self._db.add(row)  # SQLAlchemyのセッションに追加
        self._db.flush()  # flushでDBに反映させてIDを取得する
        self._db.refresh(row)  # refreshで最新の状態を取得
        return Todo(
            id=row.id, title=row.title, is_done=row.is_done
        )  # ドメインのTodoを返す

    def list(self) -> list[Todo]:  # Todoの一覧を取得するメソッドの実装
        # 論理削除されていないもののみ返す
        stmt = select(TodoModel).where(TodoModel.deleted_at == None)
        rows = self._db.execute(stmt).scalars().all()
        return [Todo(id=row.id, title=row.title, is_done=row.is_done) for row in rows]

    def update(self, todo: Todo) -> Todo:
        "既存のTodoを更新するメソッドの実装"
        stmt = select(TodoModel).where(TodoModel.id == todo.id)
        row = self._db.execute(
            stmt
        ).scalar_one_or_none()  # one_or_noneは、該当する行がなければNoneを返す

        if row is None:
            raise ValueError(f"Todo with id {todo.id} does not exist")

        # ドメインのTodoの状態をDBの行に反映
        row.title = todo.title
        row.is_done = todo.is_done

        # セッションに変更を反映
        self._db.flush()

        # 更新後のTodoを返す
        return Todo(id=row.id, title=row.title, is_done=row.is_done)

    def delete(self, id: int) -> None:
        "Todoを論理削除するメソッドの実装 (deleted_atをセット)"
        from datetime import datetime

        stmt = select(TodoModel).where(TodoModel.id == id)
        row = self._db.execute(stmt).scalar_one_or_none()
        if row is None:
            raise ValueError(f"Todo with id {id} does not exist")
        row.deleted_at = datetime.utcnow()
        self._db.flush()
        self._db.commit()
