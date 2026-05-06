from typing import List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, constr

class Book(BaseModel):
    file_name: Optional[str] = None  # optional, added after upload
    file_path: Optional[str] = None  # optional, added after upload
    id: Optional[str] = Field(None, description="Unique identifier (MongoDB ObjectId)")
    
    # Titles in multiple languages
    title: Dict[str, constr(strip_whitespace=True, min_length=1)] = Field( # type: ignore
        ..., example={"en": "Schooling Strategies", "ar": "استراتيجيات التعليم"}
    )
    
    # Type of resource
    type: constr(strip_whitespace=True, pattern="^(books|papers|book|paper)$") = Field( # type: ignore
        ..., description="Resource type: book or paper"
    )
    
    authors: List[constr(strip_whitespace=True, min_length=2)] = Field( # type: ignore
        ..., description="List of authors"
    )
    
    year: int = Field(..., ge=1900, le=2100, description="Year of publication")
    
    categories: List[str] = Field(
        ..., example=["schooling", "habits"], description="Resource categories"
    ) 
    
    language_support: List[constr(pattern="^(en|ar)$")] = Field( # type: ignore
        ..., description="Supported languages"
    )
    
    content: Dict[str, str] = Field(
        ..., description="Full text or summary in multiple languages"
    )
    
    metadata: Optional[Dict[str, str]] = Field(
        default=None,
        example={"publisher": "XYZ Press", "doi": "10.1234/example"},
        description="Additional metadata"
    )
    
    url: Optional[HttpUrl] = Field(
        None, description="Optional link to resource"
    )

    @classmethod
    def get_index(cls):
        return[
            {
                "key":[("title",1)],
                "name":"title_index",
                "ubique":True
            }
        ]


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



