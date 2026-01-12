# pythonのProtocolを使って、リポジトリのインターフェースを定義します。
from typing import Protocol
from app.domain.todo import Todo


class TodoRepository(Protocol):
    # Todoを追加するメソッドのシグネチャ
    # ...は、このメソッドが実装されていないことを示すための記法

    def add(
        self, todo: Todo
    ) -> Todo: ...  # 実際の実装はtodo_repository_sqlalchemy.pyにある

    def list(self) -> list[Todo]: ...

    def update(self, todo: Todo) -> Todo: ...
