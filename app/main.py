from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
  db.execute(text("SELECT 1"))
  return {"ok": True}