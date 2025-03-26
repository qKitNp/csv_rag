from pydantic import BaseModel
from typing import Optional

class FileResponse(BaseModel):
    file_id: str
    file_name: str
    content: str

class QueryRequest(BaseModel):
    file_id: str
    query: str

class FileContentResponse(BaseModel):
    response: str