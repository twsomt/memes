from typing import Optional

from pydantic import BaseModel, ConfigDict


class SmemeAdd(BaseModel):
    name: str
    description: Optional[str] = None


class Smeme(SmemeAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SmemeId(BaseModel):
    ok: bool = True
    meme_id: int


class SmemeUpdate(SmemeAdd):
    pass


class SmemeDelete(SmemeAdd):
    pass
