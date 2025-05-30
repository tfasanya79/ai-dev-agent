# schemas.py
from pydantic import BaseModel
from typing import Optional

class ProjectMetadata(BaseModel):
    name: str
    description: str
    url: Optional[str] = None

    class Config:
        orm_mode = True

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    design_path: Optional[str] = None

    class Config:
        orm_mode = True
