from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ベースクラスの定義 全てのデータベースモデルはこのクラスを継承する
# SQLAlchemyのDeclarativeBaseを継承してベースクラスを作成
class Base(DeclarativeBase):
    pass


class TodoModel(Base):
    # テーブル名の指定
    __tablename__ = "todos"

    # カラムの定義をここに付与する
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)


from datetime import datetime
