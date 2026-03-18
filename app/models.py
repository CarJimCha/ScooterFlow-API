from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Zona (Zone)
class Zona(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    codigo_postal = Column(String(10), nullable=False)
    limite_velocidad = Column(Integer, nullable=False)

    # Relación de 1 a muchos con Patinete
    patinetes = relationship("Patinete", back_populates="zona")

# Enum de Estados
class EstadoPatinete(str, enum.Enum):
    disponible = "disponible"
    en_uso = "en_uso"
    mantenimiento = "mantenimiento"
    sin_bateria = "sin_bateria"


# Patinete (Scooter)
class Patinete(Base):
    __tablename__ = "patinetes"

    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String)
    modelo = Column(String)
    bateria = Column(Integer)
    estado = Column(Enum(EstadoPatinete))
    puntuacion_usuario = Column(Float)

    zona_id = Column(Integer, ForeignKey("zonas.id"))

    zona = relationship("Zona", back_populates="patinetes")