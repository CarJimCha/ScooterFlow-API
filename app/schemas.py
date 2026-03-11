from pydantic import BaseModel, Field
from typing import Optional


# ---------- ZONA ----------

class ZonaBase(BaseModel):
    nombre: str
    codigo_postal: str
    limite_velocidad: int


class ZonaCreate(ZonaBase):
    pass


class Zona(ZonaBase):
    id: int

    class Config:
        from_attributes = True


# ---------- PATINETE ----------

class PatineteBase(BaseModel):
    numero_serie: str
    modelo: str
    bateria: int = Field(..., ge=0, le=100)
    estado: str
    zona_id: int


class PatineteCreate(PatineteBase):
    pass


class PatineteUpdate(BaseModel):
    modelo: Optional[str] = None
    bateria: Optional[int] = Field(None, ge=0, le=100)
    estado: Optional[str] = None
    zona_id: Optional[int] = None


class Patinete(PatineteBase):
    id: int
    puntuacion_usuario: Optional[float] = None

    class Config:
        from_attributes = True