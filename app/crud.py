from sqlalchemy.orm import Session
from app.models import Patinete, Zona
from app.schemas import PatineteCreate, PatineteUpdate, ZonaCreate


# ---------- ZONAS ----------

def get_zonas(db: Session):
    return db.query(Zona).all()


def get_zona(db: Session, zona_id: int):
    return db.query(Zona).filter(Zona.id == zona_id).first()


def create_zona(db: Session, data: ZonaCreate):
    zona = Zona(**data.model_dump())
    db.add(zona)
    db.commit()
    db.refresh(zona)
    return zona


# ---------- PATINETES ----------

def get_patinetes(db: Session):
    return db.query(Patinete).all()


def get_patinete(db: Session, patinete_id: int):
    return db.query(Patinete).filter(Patinete.id == patinete_id).first()


def create_patinete(db: Session, data: PatineteCreate):
    patinete = Patinete(**data.model_dump())
    db.add(patinete)
    db.commit()
    db.refresh(patinete)
    return patinete


def update_patinete(db: Session, patinete_id: int, data: PatineteUpdate):
    patinete = get_patinete(db, patinete_id)

    if patinete:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(patinete, key, value)

        db.commit()
        db.refresh(patinete)

    return patinete


def delete_patinete(db: Session, patinete_id: int):
    patinete = get_patinete(db, patinete_id)

    if patinete:
        db.delete(patinete)
        db.commit()

    return patinete


# ---------- ENDPOINT ESPECIAL DE LA TAREA ----------

def enviar_a_mantenimiento(db: Session, zona_id: int):
    patinetes = (
        db.query(Patinete)
        .filter(Patinete.zona_id == zona_id, Patinete.bateria < 15)
        .all()
    )

    for p in patinetes:
        p.estado = "mantenimiento"

    db.commit()

    return patinetes