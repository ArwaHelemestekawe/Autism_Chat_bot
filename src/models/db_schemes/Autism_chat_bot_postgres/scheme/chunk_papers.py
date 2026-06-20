from sqlalchemy import Column, Float, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from src.models.db_schemes.Autism_chat_bot_postgres.scheme.base_model import SQLAlchemyBase
from sqlalchemy.orm import relationship



class Chunk_papers(SQLAlchemyBase):
    __tablename__ = "chunks_papers"

    # Primary key
    id = Column(Integer, primary_key=True,autoincrement=True)

    # Reference to parent document (Book or Paper)
    document_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    paper = relationship("Papers", back_populates="chunks_papers")


    # Order of the chunk
    chunk_index = Column(Integer, nullable=False)

    # Actual text content
    content = Column(Text, nullable=False)

    # Embedding vector (can be stored as float array)
    embedding = Column(ARRAY(Float), nullable=True)

    # Metadata (page number, section, etc.)
    doc_metadata = Column("metadata", JSONB, nullable=True)



class RetrivedOcument():
    content:str
    score:float