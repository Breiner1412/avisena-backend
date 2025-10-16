from pydantic import BaseModel, Field
from typing import Optional

class ShedBase(BaseModel):
    id_finca: int
    nombre: str = Field(min_length=3, max_length=70)
    capacidad: float
    cant_actual: float
    estado: bool

class ShedCreate(ShedBase):
    pass

class ShedUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=80)
    capacidad: Optional[float]
    cant_actual: Optional[float]

class ShedEstado(BaseModel):
    estado: Optional[bool] = None

class ShedOut(ShedBase):
    id_galpon: int
    id_finca: int