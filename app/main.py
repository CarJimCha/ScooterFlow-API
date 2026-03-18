from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app.schemas import (
    PatineteCreate,
    PatineteUpdate,
    Patinete,
    ZonaCreate,
    Zona
)

app = FastAPI(
    title="ScooterFlow API",
    version="1.0.0",
    description="API para gestión de patinetes eléctricos"
)

# -----------------------------
# ROOT
# -----------------------------

@app.get("/")
def read_root():
    return {"message": "App ScooterFlow-API v3.0"}


# -----------------------------
# ZONAS
# -----------------------------

@app.get("/zonas", response_model=list[Zona])
def listar_zonas(db: Session = Depends(get_db)):
    return crud.get_zonas(db)


@app.get("/zonas/{zona_id}", response_model=Zona)
def obtener_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = crud.get_zona(db, zona_id)
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona


@app.post("/zonas", response_model=Zona, status_code=status.HTTP_201_CREATED)
def crear_zona(data: ZonaCreate, db: Session = Depends(get_db)):
    return crud.create_zona(db, data)


@app.delete("/zonas/{zona_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = crud.delete_zona(db, zona_id)
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return


# -----------------------------
# PATINETES
# -----------------------------

@app.get("/patinetes", response_model=list[Patinete])
def listar_patinetes(db: Session = Depends(get_db)):
    return crud.get_patinetes(db)


@app.get("/patinetes/{patinete_id}", response_model=Patinete)
def obtener_patinete(patinete_id: int, db: Session = Depends(get_db)):
    patinete = crud.get_patinete(db, patinete_id)
    if not patinete:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    return patinete


@app.post("/patinetes", response_model=Patinete, status_code=status.HTTP_201_CREATED)
def crear_patinete(data: PatineteCreate, db: Session = Depends(get_db)):
    return crud.create_patinete(db, data)


@app.put("/patinetes/{patinete_id}", response_model=Patinete)
def actualizar_patinete(
    patinete_id: int,
    data: PatineteUpdate,
    db: Session = Depends(get_db)
):
    patinete = crud.update_patinete(db, patinete_id, data)
    if not patinete:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    return patinete


@app.delete("/patinetes/{patinete_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_patinete(patinete_id: int, db: Session = Depends(get_db)):
    patinete = crud.delete_patinete(db, patinete_id)
    if not patinete:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    return


# -----------------------------
# ENDPOINT ESPECIAL
# -----------------------------

@app.post("/zonas/{zona_id}/mantenimiento")
def patinetes_a_mantenimiento(zona_id: int, db: Session = Depends(get_db)):

    actualizados = crud.enviar_a_mantenimiento(db, zona_id)

    return {
        "cantidad": actualizados
    }