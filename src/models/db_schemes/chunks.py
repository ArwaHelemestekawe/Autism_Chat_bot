from typing import Optional, Dict, List, Union
from pydantic import BaseModel, Field

class Chunk(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier (MongoDB ObjectId)")
    
    document_id: str = Field(...,description=" type of document")
    document_name:str= Field(..., description="title of the document")
    
    chunk_index: int = Field(..., ge=0, description="Order of the chunk within the book")
    
    content: str = Field(
        ..., 
        description="content"
    )
    
    embedding: Optional[List[float]] = Field(
        None, description="Vector embedding for retrieval (if using RAG)"
    )
    
    metadata: Optional[Dict[str, Union[str,int]]] = Field(
        None, description="Optional per-chunk metadata (e.g., page number, section)"
    )

    @classmethod
    def get_index(cls):
        return[
            {
                "key":[("document_name",1)],
                "name":"title_index",
                "unique":False
            }
        ]
'''
Workflow
Insert the Book document once with all metadata.

Split the book into chunks.

Insert each Chunk document, referencing the book_id.

This way, your chatbot can:

Search embeddings in chunks for answers.

Pull metadata from the parent book when needed (e.g., show title, author).
'''