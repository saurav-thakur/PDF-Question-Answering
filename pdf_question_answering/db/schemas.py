from pydantic import BaseModel


class Question(BaseModel):
    question: str


class PDFMetaDataBase(BaseModel):
    filename: str
    upload_date: str

    class Config:
        from_attributes = True  # Allow compatibility with ORM models for responses
