from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.lands import LandCreate, LandOut, LandUpdate
from app.crud import lands as crud_lands

router = APIRouter()

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_land(
    land: LandCreate,
    db: Session = Depends(get_db),
    user_token: LandOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol        
        if not verify_permissions(db, id_rol, 3, 'insertar'):
            raise HTTPException(status_code=401, detail="usuario no autorizado para crear finca")

        crud_lands.create_land(db, land)
        return {"message": "Finca creada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-name", response_model=LandOut)
def get_land(
    name: str,
    db: Session = Depends(get_db),
    user_token: LandOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol        
        if not verify_permissions(db, id_rol, 3, 'seleccionar'):
            raise HTTPException(status_code=401, detail="usuario no autorizado para ver finca")

        land = crud_lands.get_land_by_name(db, name)
        if not land:
            raise HTTPException(status_code=404, detail="Finca no encontrada")
        return land
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.get("/all", response_model=LandOut)
# def get_lands(
#     db: Session = Depends(get_db),
#     user_token: LandOut = Depends(get_current_user)
# ):
#     try:
#         id_rol = user_token.id_rol        
#         if not verify_permissions(db, id_rol, 3, 'seleccionar'):
#             raise HTTPException(status_code=401, detail="usuario no autorizado para consultar fincas")

#         land = crud_lands.get_all_lands(db)
#         if not land:
#             raise HTTPException(status_code=404, detail="No hay fincas")
#         return land
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{user_id}")
def update_land(
    user_id: int,
    land: LandUpdate,
    db: Session = Depends(get_db),
    user_token: LandOut = Depends(get_current_user)
):
    try:
        success = crud_lands.update_land_by_id(db, user_id, land)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la finca")
        return {"message": "Finca actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

