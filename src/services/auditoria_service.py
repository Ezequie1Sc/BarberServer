from extensions import db
from src.models.auditoria_login import AuditoriaLogin
from datetime import date
import logging

logger = logging.getLogger(__name__)

class AuditoriaService:
    
    @staticmethod
    def get_all_logs():
        """Get all login audit logs"""
        try:
            logs = AuditoriaLogin.query.all()
            return [log.to_dict() for log in logs], 200
        except Exception as e:
            logger.error(f"Error al obtener logs: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def create_log(data, request):
        """Create a new audit log"""
        try:
            nuevo_log = AuditoriaLogin(
                id_user=data.get('id_user'),
                usuario_ingresado=data['usuario_ingresado'].strip(),
                exito=data['exito'],
                ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent', 'Desconocido')
            )
            
            db.session.add(nuevo_log)
            db.session.commit()
            logger.info(f"Log creado: ID {nuevo_log.id}")
            return nuevo_log.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear log: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def get_failed_logs():
        """Get all failed login attempts"""
        try:
            logs = AuditoriaLogin.query.filter_by(exito=False).all()
            return [log.to_dict() for log in logs], 200
        except Exception as e:
            logger.error(f"Error al obtener logs fallidos: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def get_today_logs():
        """Get today's login attempts"""
        try:
            today = date.today()
            logs = AuditoriaLogin.query.filter(
                db.func.date(AuditoriaLogin.fecha) == today
            ).all()
            return [log.to_dict() for log in logs], 200
        except Exception as e:
            logger.error(f"Error al obtener logs del día: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500