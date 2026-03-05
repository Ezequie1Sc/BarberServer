from extensions import db
from src.models.usuario import Usuario
from src.models.auditoria_login import AuditoriaLogin
from src.utils.validators import Validators
import logging

logger = logging.getLogger(__name__)

class UsuarioService:
    
    @staticmethod
    def create_usuario(data):
        """Create a new user"""
        try:
            # Check if user or email already exists
            if Usuario.query.filter_by(Usuario=data['Usuario'].strip()).first():
                return {'error': 'El nombre de usuario ya está en uso'}, 400
            
            if Usuario.query.filter_by(Email=data['Email'].strip()).first():
                return {'error': 'El correo electrónico ya está registrado'}, 400
            
            # Create new user
            nuevo_usuario = Usuario(
                Usuario=data['Usuario'].strip(),
                Nombre=data['Nombre'].strip(),
                Apellido=data['Apellido'].strip(),
                Email=data['Email'].strip(),
                Telefono=data.get('Telefono', '').strip(),
                Passsword=data['Passsword']
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            logger.info(f"Usuario creado exitosamente: ID {nuevo_usuario.IdUser}")
            return nuevo_usuario.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear usuario: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def get_all_usuarios():
        """Get all users"""
        try:
            usuarios = Usuario.query.all()
            return [usuario.to_dict() for usuario in usuarios], 200
        except Exception as e:
            logger.error(f"Error al obtener usuarios: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def update_usuario(id, data):
        """Update a user"""
        try:
            usuario = Usuario.query.get(id)
            if not usuario:
                return {'error': 'Usuario no encontrado'}, 404
            
            # Update fields
            if 'Usuario' in data:
                if data['Usuario'] != usuario.Usuario and Usuario.query.filter_by(Usuario=data['Usuario']).first():
                    return {'error': 'El nombre de usuario ya está en uso'}, 400
                usuario.Usuario = data['Usuario'].strip()
            
            if 'Email' in data:
                if data['Email'] != usuario.Email and Usuario.query.filter_by(Email=data['Email']).first():
                    return {'error': 'El correo electrónico ya está registrado'}, 400
                usuario.Email = data['Email'].strip()
            
            # Update other fields
            if 'Nombre' in data:
                usuario.Nombre = data['Nombre'].strip()
            if 'Apellido' in data:
                usuario.Apellido = data['Apellido'].strip()
            if 'Telefono' in data:
                usuario.Telefono = data['Telefono'].strip()
            if 'Passsword' in data:
                usuario.Passsword = data['Passsword']
            
            db.session.commit()
            logger.info(f"Usuario actualizado: ID {id}")
            return usuario.to_dict(), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar usuario: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def delete_usuario(id):
        """Delete a user"""
        try:
            usuario = Usuario.query.get(id)
            if not usuario:
                return {'error': 'Usuario no encontrado'}, 404
            
            db.session.delete(usuario)
            db.session.commit()
            logger.info(f"Usuario eliminado: ID {id}")
            return {'message': 'Usuario eliminado correctamente'}, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar usuario: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def login(credentials, request):
        """Authenticate user and log attempt"""
        try:
            usuario = Usuario.query.filter_by(Usuario=credentials['Usuario'].strip()).first()
            login_success = usuario and usuario.Passsword == credentials['Passsword']
            
            # Log the attempt
            auditoria = AuditoriaLogin(
                id_user=usuario.IdUser if login_success else None,
                usuario_ingresado=credentials['Usuario'].strip(),
                exito=login_success,
                ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent', 'Desconocido')
            )
            db.session.add(auditoria)
            db.session.commit()
            
            if login_success:
                logger.info(f"Login exitoso: ID {usuario.IdUser}")
                return usuario.to_dict(), 200
            else:
                logger.warning(f"Login fallido: {credentials['Usuario']}")
                return {'error': 'Usuario o contraseña incorrectos'}, 401
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error en login: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500