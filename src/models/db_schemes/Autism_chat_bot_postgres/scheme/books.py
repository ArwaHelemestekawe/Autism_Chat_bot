from src.models.db_schemes.Autism_chat_bot_postgres.scheme.base_model import SQLAlchemyBase
from sqlalchemy import column ,Integer
from sqlalchemy import Column, Integer, String, Text, JSON, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship

class Books(SQLAlchemyBase):

    __tablename__ = "books"   # Table name in Postgres

    id=Column(Integer, primary_key=True,autoincrement=True)


    document_id = Column(String, primary_key=False)  # Could be UUID instead of Mongo ObjectId
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    chunks_books = relationship ("Chunk_books", back_populates="book")
    # Titles  → String
    title = Column(String, nullable=False)

    # Authors → array of strings
    authors = Column(ARRAY(String), nullable=False)

    # Year of publication
    year = Column(Integer, nullable=False)

    # Categories → array of strings
    categories = Column(ARRAY(String), nullable=False)

    # Supported languages → array of strings
    language_support = Column(ARRAY(String), nullable=False)

    # Content in multiple languages → JSON field   just a brief 
    content = Column(JSONB, nullable=False)

    # Metadata → JSON field
    doc_metadata = Column("metadata", JSONB, nullable=True)

    # Optional URL
    url = Column(String, nullable=True)












'''
{
  "title": {
    "en": "The Reason I Jump",
    "ar": "السبب الذي أقفز من أجله"
  },
  "type": "book",
  "authors": ["Naoki Higashida"],
  "year": 2007,
  "categories": ["Autism", "Memoir", "Psychology"],
  "language_support": ["en", "ar"],
  "content": {
    "en": "A memoir written by Naoki Higashida, a thirteen-year-old boy with autism, offering insight into the inner world of autistic individuals.",
    "ar": "مذكرات كتبها ناوكي هيغاشيدا، وهو طفل في الثالثة عشرة مصاب بالتوحد، يقدم فيها رؤية عن العالم الداخلي للأشخاص المصابين بالتوحد."
  },
  "metadata": {
    "publisher": "XYZ Press"
  }
}


'''



