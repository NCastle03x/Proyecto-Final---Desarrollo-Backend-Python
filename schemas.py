from pydantic import BaseModel, Field
from typing import Optional

class ResenaBase(BaseModel):
    cliente: str
    comentario: str
    calificacion: int = Field(..., ge=1, le=5)

class ResenaCreate(ResenaBase):
    pass

class ResenaResponse(ResenaBase):
    id: int
    sentimiento: Optional[str] = None

    class Config:
        from_attributes = True
