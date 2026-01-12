# ドメイン層では、Todoのルールを定義します。
# 例えば、タイトルの最大長や必須項目などのバリデーションをここで行います。


from dataclasses import dataclass


# @dataclassを作ることで、Pythonにこのクラスはデータを保持するためのものであることを伝えます。
# frozen=Trueを指定することで、インスタンス生成後に属性を書き換えることを防ぎます。
@dataclass(frozen=True)
# フィールド定義。Todoが持つべき属性をここに定義します。
class Todo:
    id: int
    title: str
    is_done: bool

    # Todoインスタンスを生成するためのファクトリーメソッド
    # ここでバリデーションを行い、正しい状態のTodoインスタンスのみを生成します。
    # title:strを渡してTodoインスタンスを生成する
    @staticmethod
    def new(title: str) -> "Todo":
        # .strip()で前後の空白を削除
        normalized = title.strip()

        # バリデーション: titleは空であってはいけない、200文字以内であること
        if not normalized:
            raise ValueError("title must not be empty")
        if len(normalized) > 200:
            raise ValueError("title must be <= 200 characters")
        # バリデーションを通過したら、idは0（未保存状態を示す）、is_doneはFalseでTodoインスタンスを生成して返す
        return Todo(id=0, title=normalized, is_done=False)
