from fastapi import Depends
from sqlalchemy.orm import Session
from pdf_question_answering.db.database import SessionLocal
from typing import Annotated


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
