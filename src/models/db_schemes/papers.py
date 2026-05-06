from typing import List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, constr

class Paper(BaseModel):
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

'''
{
  "title": {
    "en": "New advances in the diagnosis and treatment of autism spectrum disorders",
    "ar": "تطورات جديدة في تشخيص وعلاج اضطرابات طيف التوحد"
  },
  "type": "papers",
  "authors": ["Lei Qin", "Haijiao Wang", "Wenjing Ning", "Mengmeng Cui", "Qian Wang"],
  "year": 2024,
  "categories": ["autism", "diagnosis", "treatment"],
  "language_support": ["en", "ar"],
  "content": {
    "en": "Review article discussing recent progress in diagnosis and treatment of autism spectrum disorders.",
    "ar": "مقال مراجعة يناقش أحدث التطورات في تشخيص وعلاج اضطرابات طيف التوحد."
  },
  "metadata": {
    "publisher": "European Journal of Medical Research",
    "doi": "10.1186/s40001-024-01916-2"
  }
}
'''