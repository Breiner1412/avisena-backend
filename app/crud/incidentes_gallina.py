from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging
from app.schemas.incidentes_gallina import IncidenteGallinaCreate, IncidenteGallinaUpdate

logger = logging.getLogger(__name__)

# Crear incidente de gallina
def create_incidente(db: Session, incidente: IncidenteGallinaCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO incidentes_gallina (
                galpon_origen, tipo_incidente, cantidad, descripcion, fecha_hora, esta_resuelto
            ) VALUES (
                :galpon_origen, :tipo_incidente, :cantidad, :descripcion, :fecha_hora, :esta_resuelto
            )
        """)
        db.execute(sentencia, incidente.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear incidente de gallina: {e}")
        raise Exception("Error de base de datos al crear incidente de gallina")

# Obtener incidente por ID
def get_incidente_by_id(db: Session, id_inc_gallina: int):
    try:
        query = text("""
            SELECT id_inc_gallina, galpon_origen, tipo_incidente, cantidad, descripcion, fecha_hora, esta_resuelto
            FROM incidentes_gallina
            WHERE id_inc_gallina = :id_inc_gallina
        """)
        result = db.execute(query, {"id_inc_gallina": id_inc_gallina}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener incidente de gallina por ID: {e}")
        raise Exception("Error al consultar incidente de gallina por ID")

# Obtener todos los incidentes
def get_all_incidentes(db: Session):
    try:
        query = text("""
            SELECT id_inc_gallina, galpon_origen, tipo_incidente, cantidad, descripcion, fecha_hora, esta_resuelto
            FROM incidentes_gallina
            ORDER BY fecha_hora DESC
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener incidentes de gallinas: {e}")
        raise Exception("Error al listar incidentes de gallinas")

# Actualizar incidente
def update_incidente_by_id(db: Session, id_inc_gallina: int, incidente: IncidenteGallinaUpdate) -> Optional[bool]:
    try:
        fields = incidente.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields.keys()])
        sentencia = text(f"""
            UPDATE incidentes_gallina
            SET {set_clause}
            WHERE id_inc_gallina = :id_inc_gallina
        """)
        fields["id_inc_gallina"] = id_inc_gallina
        result = db.execute(sentencia, fields)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar incidente de gallina {id_inc_gallina}: {e}")
        raise Exception("Error de base de datos al actualizar incidente de gallina")

# Eliminar incidente
def toggle_estado_incidente(db: Session, id_inc_gallina: int):
    try:
        query = text("""
            UPDATE incidentes_gallina
            SET esta_resuelto = NOT esta_resuelto
            WHERE id_inc_gallina = :id_inc_gallina
        """)
        result = db.execute(query, {"id_inc_gallina": id_inc_gallina})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado del incidente de gallina: {e}")
        raise Exception("Error de base de datos al actualizar estado del incidente")

