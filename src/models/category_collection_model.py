
from typing import Optional

from pydantic import BaseModel, Field


class Category(BaseModel):
    id: Optional[str] = Field(None)
    name: str = Field(..., description="Category name, e.g. books or papers")
