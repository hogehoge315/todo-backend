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
        stmt = select(TodoModel)  # TodoModelを選択するSQL文を作成 stmtはstatementの略
        rows = (
            self._db.execute(stmt)  # executeでSQLを実行
            .scalars()  # scalars()で結果をオブジェクトに変換
            .all()  # all()で全件取得
        )  # SQLAlchemyのセッションで実行して結果を取得
        return [
            Todo(id=row.id, title=row.title, is_done=row.is_done) for row in rows
        ]  # ドメインのTodoのリストを返す
