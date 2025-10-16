from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IncidenteGallinaBase(BaseModel):
    galpon_origen: int
    tipo_incidente: str = Field(..., min_length=3, max_length=50)
    cantidad: int = Field(..., gt=0)
    descripcion: str = Field(..., min_length=5, max_length=255)
    fecha_hora: datetime
    esta_resuelto: bool = Field(default=False)

class IncidenteGallinaCreate(IncidenteGallinaBase):
    pass

class IncidenteGallinaUpdate(BaseModel):
    galpon_origen: Optional[int] = None
    tipo_incidente: Optional[str] = Field(default=None, min_length=3, max_length=50)
    cantidad: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, min_length=5, max_length=255)
    fecha_hora: Optional[datetime] = None
    esta_resuelto: Optional[bool] = None

class IncidenteGallinaOut(IncidenteGallinaBase):
    id_inc_gallina: int
