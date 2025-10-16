from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from core.security import get_hashed_password
import logging

from app.schemas.lands import LandCreate, LandUpdate

logger = logging.getLogger(__name__)

def create_land(db: Session, land: LandCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO fincas(
                nombre, longitud, latitud,
                id_usuario, estado
            ) VALUES (
                :nombre, :longitud, :latitud,
                :id_usuario, :estado
            )
        """)
        db.execute(sentencia, land.model_dump())
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear finca: {e}")
        raise Exception("Error de base de datos al crear la finca")

def get_land_by_name(db: Session, name: str):
    try:
        query = text("""SELECT id_finca, nombre, longitud, latitud, id_usuario, estado
                     FROM fincas
                     WHERE fincas.nombre = :nombre_finca
                """)
        result = db.execute(query, {"nombre_finca": name}).mappings().first()
        return result
    except Exception as e:
        logger.error(f"Error al obtener finca por nombre: {e}")
        raise Exception("Error de base de datos al obtener la finca")
    
# def get_all_lands(db: Session):
#     try:
#         query = text("""SELECT id_finca, fincas.nombre, longitud, latitud, fincas.id_usuario, fincas.estado, usuarios.nombre
#                      FROM fincas INNER JOIN usuarios ON usuarios.id_usuario=fincas.id_usuario
#                 """)
#         result = db.execute(query).mappings().all()
#         return result
#     except Exception as e:
#         logger.error(f"Error al obtener fincas: {e}")
#         raise Exception("Error de base de datos al obtener las fincas")

    
def update_land_by_id(db: Session, land_id: int, land: LandUpdate) -> Optional[bool]:
    try:
        # Solo los campos enviados por el cliente
        land_data = land.model_dump(exclude_unset=True)
        if not land_data:
            return False  # nada que actualizar

        # Construir dinámicamente la sentencia UPDATE
        set_clauses = ", ".join([f"{key} = :{key}" for key in land_data.keys()])
        sentencia = text(f"""
            UPDATE fincas 
            SET {set_clauses}
            WHERE id_finca = :id_finca
        """)

        # Agregar el id_finca
        land_data["id_finca"] = land_id

        result = db.execute(sentencia, land_data)
        db.commit()

        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar finca {land_id}: {e}")
        raise Exception("Error de base de datos al actualizar la finca")

# def get_land_by_id(db:Session, id:int):
#     try:
#         query = text("""SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
#                      FROM usuarios INNER JOIN roles ON usuarios.id_rol=roles.id_rol
#                      WHERE id_usuario = :id_land
#                 """)
#         result = db.execute(query, {"id_land": id}).mappings().first()
#         return result
#     except Exception as e:
#         logger.error(f"Error al obtener usuario por email: {e}")
#         raise Exception("Error de base de datos al obtener el usuario")