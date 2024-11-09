from sqlalchemy import String, Integer, Column
from pdf_question_answering.db.database import Base


class PDFData(Base):
    __tablename__ = "pdfmetadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(String, index=True)
