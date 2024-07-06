from typing import Optional

from pydantic import BaseModel


class SmemeAdd(BaseModel):
    description: Optional[str] = None


class Smeme(BaseModel):
    id: int
    image_path: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class SmemeUpdate(SmemeAdd):
    id: int


class SmemeDelete(BaseModel):
    id: int
