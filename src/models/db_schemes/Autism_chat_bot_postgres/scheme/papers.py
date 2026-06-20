from src.models.db_schemes.Autism_chat_bot_postgres.scheme.base_model import SQLAlchemyBase
from sqlalchemy import column ,Integer
from sqlalchemy import Column, Integer, String, Text, JSON, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship




class Papers(SQLAlchemyBase):
    __tablename__ = "papers"   # Table name in Postgres
    id = Column(Integer, primary_key=True,autoincrement=True)

    # Primary key (could be UUID instead of Mongo ObjectId)
    document_id = Column(String, primary_key=False)

    # Optional file info
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)

    title = Column(String, nullable=False)

    # Type of resource (book/paper)
    type = Column(String, nullable=False)
    chunks_papers = relationship("Chunk_papers", back_populates="paper")

    # Authors → array of strings
    authors = Column(ARRAY(String), nullable=False)

    # Year of publication
    year = Column(Integer, nullable=False)

    # Categories → array of strings
    categories = Column(ARRAY(String), nullable=False)

    # Supported languages → array of strings
    language_support = Column(ARRAY(String), nullable=False)

    # Content in multiple languages → JSON field
    content = Column(JSONB, nullable=False)

    # Metadata → JSON field
    

    doc_metadata = Column("metadata", JSONB, nullable=True)# Optional URL
    url = Column(String, nullable=True)
