from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud import incidentes_gallina as crud_incidentes
from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from app.schemas.users import UserOut
from app.schemas.incidentes_gallina import (
    IncidenteGallinaCreate, IncidenteGallinaUpdate, IncidenteGallinaOut
)
from core.database import get_db

router = APIRouter()
modulo = 7

# Crear incidente de gallina
@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_incidente(
    incidente: IncidenteGallinaCreate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        crud_incidentes.create_incidente(db, incidente)
        return {"message": "Incidente de gallina creado correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener incidente por ID
@router.get("/by-id/{id_inc_gallina}", response_model=IncidenteGallinaOut)
def get_incidente(
    id_inc_gallina: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        incidente = crud_incidentes.get_incidente_by_id(db, id_inc_gallina)
        if not incidente:
            raise HTTPException(status_code=404, detail="Incidente no encontrado")
        return incidente

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Listar todos los incidentes
@router.get("/all", response_model=list[IncidenteGallinaOut])
def get_all_incidentes(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        incidentes = crud_incidentes.get_all_incidentes(db)
        return incidentes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Actualizar incidente
@router.put("/by-id/{id_inc_gallina}")
def update_incidente(
    id_inc_gallina: int,
    incidente: IncidenteGallinaUpdate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        success = crud_incidentes.update_incidente_by_id(db, id_inc_gallina, incidente)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el incidente")

        return {"message": "Incidente actualizado correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Eliminar incidente
@router.put("/cambiar-estado/{id_inc_gallina}")
def cambiar_estado_incidente(
    id_inc_gallina: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        actualizado = crud_incidentes.toggle_estado_incidente(db, id_inc_gallina)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Incidente no encontrado")

        return {"message": "Estado del incidente de gallina cambiado correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


