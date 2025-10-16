from pydantic import BaseModel, Field
from typing import Optional

class LandBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=30)
    longitud: float
    latitud: float
    id_usuario: int
    estado: bool

class LandCreate(LandBase):
    pass

class LandUpdate(BaseModel):    
    nombre: Optional [str] = Field(default=None, min_length=3, max_length=30)
    longitud: Optional [float] = None
    latitud: Optional [float] = None
    id_usuario: Optional [str] = Field(default=None, min_length=1, max_length=2)
    estado: Optional [bool] = None

class LandEstado(BaseModel):
    estado: Optional[bool] = None

class LandOut(LandBase):
    id_finca: int
    # nombre_usuario: str
