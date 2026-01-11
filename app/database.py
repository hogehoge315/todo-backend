import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
  raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal() # ここでセッションを作成
  try:
    yield db # セッションを返す
  finally:
    db.close() # セッションを閉じる(セッションを閉じないと、接続がリークする可能性がある)
