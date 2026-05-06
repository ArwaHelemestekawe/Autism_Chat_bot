from pydantic import BaseModel
from typing import Optional
class ProcssRequest(BaseModel):
    chunk_size:Optional[int]=100
    over_lap_size:Optional[int]=20
    file_name:str