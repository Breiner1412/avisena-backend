from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from core.security import get_hashed_password
import logging

from app.schemas.users import UserCreate, UserUpdate

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> Optional[bool]:
    try:
        pass_encript=get_hashed_password(user.pass_hash)
        user.pass_hash=pass_encript
        sentencia = text("""
            INSERT INTO usuarios(
                nombre, id_rol, email,
                telefono, documento,   
                pass_hash, estado
            ) VALUES (
                :nombre, :id_rol, :email,
                :telefono, :documento,
                :pass_hash, :estado
            )
        """)
        db.execute(sentencia, user.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")

def get_user_by_email_for_login(db: Session, email: str):
    try:
        query = text("""SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol, pass_hash
                     FROM usuarios INNER JOIN roles ON usuarios.id_rol=roles.id_rol
                     WHERE email = :correo
                """)
        result = db.execute(query, {"correo": email}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")

def get_user_by_email(db: Session, email: str):
    try:
        query = text("""SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
                     FROM usuarios INNER JOIN roles ON usuarios.id_rol=roles.id_rol
                     WHERE email = :correo
                """)
        result = db.execute(query, {"correo": email}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")

def get_all_user_except_admins(db: Session):
    try:
        query = text("""SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
                     FROM usuarios INNER JOIN roles ON usuarios.id_rol=roles.id_rol
                     WHERE usuarios.id_rol NOT IN (1,2)
                """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios: {e}")
        raise Exception("Error de base de datos al obtener los usuarios")

# def update_user_by_id(db: Session, user_id: int, user_update: UserUpdate) -> bool:
#     try:
#         fields = user_update.model_dump(exclude_unset=True)
#         if not fields:
#             return False
#         set_clause = ", ".join([f"{key} = :{key}" for key in fields])
#         fields["user_id"] = user_id

#         query = text(f"UPDATE usuarios SET {set_clause} WHERE id_usuario = :user_id")
#         db.execute(query, fields)
#         db.commit()
#         return True
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error al actualizar usuario: {e}")
#         raise Exception("Error de base de datos al actualizar el usuario")

def update_user_by_id(db: Session, user_id: int, user: UserUpdate) -> Optional[bool]:
    try:
        # Solo los campos enviados por el cliente
        user_data = user.model_dump(exclude_unset=True)
        if not user_data:
            return False  # nada que actualizar

        # Construir dinámicamente la sentencia UPDATE
        set_clauses = ", ".join([f"{key} = :{key}" for key in user_data.keys()])
        sentencia = text(f"""
            UPDATE usuarios 
            SET {set_clauses}
            WHERE id_usuario = :id_usuario
        """)

        # Agregar el id_usuario
        user_data["id_usuario"] = user_id

        result = db.execute(sentencia, user_data)
        db.commit()

        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario {user_id}: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")

def get_user_by_id(db:Session, id:int):
    try:
        query = text("""SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
                     FROM usuarios INNER JOIN roles ON usuarios.id_rol=roles.id_rol
                     WHERE id_usuario = :id_user
                """)
        result = db.execute(query, {"id_user": id}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")