from pydantic import BaseModel, Field
from datetime import datetime

class RegistroSensorBase(BaseModel):
    id_sensor: int
    dato_sensor: float
    fecha_hora: datetime
    u_medida: str = Field(..., min_length=1, max_length=10)

class RegistroSensorCreate(RegistroSensorBase):
    pass

class RegistroSensorOut(RegistroSensorBase):
    id_registro: int
    nombre_sensor: str | None = None  # viene del JOIN
