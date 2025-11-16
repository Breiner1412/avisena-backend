from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.incidentes_generales import IncidenteGeneralCreate, IncidenteGeneralUpdate

logger = logging.getLogger(__name__)

# Crear incidente general
def create_incidente(db: Session, incidente: IncidenteGeneralCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO incidentes_generales (
                descripcion, fecha_hora, id_finca, esta_resuelta
            ) VALUES (
                :descripcion, :fecha_hora, :id_finca, :esta_resuelta
            )
        """)
        db.execute(sentencia, incidente.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear incidente general: {e}")
        raise Exception("Error de base de datos al crear incidente general")

# Obtener incidente por ID
def get_incidente_by_id(db: Session, id_incidente: int):
    try:
        query = text("""
            SELECT 
                ig.id_incidente, 
                ig.descripcion, 
                ig.fecha_hora, 
                ig.id_finca, 
                ig.esta_resuelta,
                f.nombre AS nombre_finca  -- Agregar el nombre de la finca
            FROM incidentes_generales ig
            LEFT JOIN fincas f ON ig.id_finca = f.id_finca
            WHERE ig.id_incidente = :id_incidente
        """)
        result = db.execute(query, {"id_incidente": id_incidente}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener incidente general por ID: {e}")
        raise Exception("Error al consultar incidente general por ID")

# Obtener todos los incidentes
# Obtener todos los incidentes con paginación
# En tu archivo CRUD - función actualizada
def get_all_incidentes(db: Session, skip: int = 0, limit: int = 100):
    try:
        # Consulta para obtener el total de registros
        count_query = text("""
            SELECT COUNT(*) as total
            FROM incidentes_generales ig
            LEFT JOIN fincas f ON ig.id_finca = f.id_finca
        """)
        total = db.execute(count_query).scalar()

        # Consulta principal con paginación
        query = text("""
            SELECT 
                ig.id_incidente, 
                ig.descripcion, 
                ig.fecha_hora, 
                ig.id_finca, 
                ig.esta_resuelta,
                f.nombre AS nombre_finca
            FROM incidentes_generales ig
            LEFT JOIN fincas f ON ig.id_finca = f.id_finca
            ORDER BY ig.fecha_hora DESC
            LIMIT :limit OFFSET :skip
        """)
        result = db.execute(query, {"skip": skip, "limit": limit}).mappings().all()
        
        # Convertir a lista de diccionarios para compatibilidad con Pydantic
        incidentes_list = [dict(incidente) for incidente in result]
        
        return {
            "incidentes": incidentes_list,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener incidentes generales: {e}")
        raise Exception("Error al listar incidentes generales")
# Actualizar incidente
def update_incidente_by_id(db: Session, id_incidente: int, incidente: IncidenteGeneralUpdate) -> Optional[bool]:
    try:
        fields = incidente.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields.keys()])
        sentencia = text(f"""
            UPDATE incidentes_generales
            SET {set_clause}
            WHERE id_incidente = :id_incidente
        """)
        fields["id_incidente"] = id_incidente
        result = db.execute(sentencia, fields)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar incidente general {id_incidente}: {e}")
        raise Exception("Error de base de datos al actualizar incidente general")

# Eliminar incidente
def toggle_estado_incidente(db: Session, id_incidente: int):
    try:
        query = text("""
            UPDATE incidentes_generales
            SET esta_resuelta = NOT esta_resuelta
            WHERE id_incidente = :id_incidente
        """)
        result = db.execute(query, {"id_incidente": id_incidente})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado del incidente general: {e}")
        raise Exception("Error de base de datos al actualizar estado del incidente")

