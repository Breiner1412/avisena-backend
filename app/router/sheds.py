from app.schemas.sheds import ShedOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.schemas.sheds import ShedCreate, ShedUpdate
from app.crud import sheds as crud_sheds
from app.router.dependencies import get_current_user
from app.crud.permisos import verify_permissions
from typing import List



router = APIRouter()
modulo = 1

@router.post("/crear-galpon", status_code=status.HTTP_201_CREATED)
def create_shed(
    shed: ShedCreate,
    user: ShedOut = Depends(get_current_user), 
    db: Session = Depends(get_db),
    shed_token: ShedOut = Depends(get_current_user)
):
    try:
        #El rol quien usa el endpoint
        id_rol = shed_token.id_rol
        if (user.id_rol == 1 or user.id_rol == 2):
            modulo = 2
        else:
            modulo = 1

        if not verify_permissions(db, id_rol, modulo, 'insertar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
            
        crud_sheds.create_shed(db, shed)
        return {"message": "Galpón creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/by-id", response_model = ShedOut)
def get_shed(
    id: int, 
    db: Session = Depends(get_db),
    shed_token: ShedOut = Depends(get_current_user)
):
    try:
        id_rol = shed_token.id_rol
        if not id == shed_token.id_usuario:
            if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
                raise HTTPException(status_code=401, detail="Usuario no autorizado")
        shed = crud_sheds.get_shed_by_id(db, id)
        if not shed:
            raise HTTPException(status_code=404, detail="Galpón no encontrada")
        return shed
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/by-id/{shed_id}")
def update_shed(
    shed_id: int, 
    shed: ShedUpdate, 
    db: Session = Depends(get_db),
    shed_token: ShedOut = Depends(get_current_user)
):
    try:
        id_rol = shed_token.id_rol

        if not verify_permissions(db, id_rol, modulo, 'actualizar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        success = crud_sheds.update_shed_by_id(db, shed_id, shed)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el galpón")
        return {"message": "Galpón actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/cambiar-estado/{id_galpon}", status_code=status.HTTP_200_OK)
def change_shed_status(
    id_galpon: int,
    nuevo_estado: bool,
    db: Session = Depends(get_db),
    shed_token: ShedOut = Depends(get_current_user)
):
    try:
        # Verificar permisos del usuario
        id_rol = shed_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'actualizar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        success = crud_sheds.change_shed_status(db, id_galpon, nuevo_estado)
        if not success:
            raise HTTPException(status_code=404, detail="Galpón no encontrado")

        return {"message": f"Estado del galpón actualizado a {nuevo_estado}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))