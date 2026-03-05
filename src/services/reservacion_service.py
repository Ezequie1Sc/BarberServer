from extensions import db
from src.models.reservacion import Reservacion
from src.models.usuario import Usuario
from src.utils.validators import Validators
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ReservacionService:
    
    @staticmethod
    def create_reservacion(data):
        """Create a new reservation"""
        try:
            # Validate user exists
            if not Usuario.query.get(data['IdUser']):
                return {'error': 'El usuario especificado no existe'}, 400
            
            # Parse and validate date/time
            try:
                fecha = datetime.strptime(data['Fecha'], '%Y-%m-%d').date()
                hora = datetime.strptime(data['Hora'], '%H:%M').time()
            except ValueError:
                return {'error': 'Formato de fecha (YYYY-MM-DD) u hora (HH:MM) inválido'}, 400
            
            # Validations
            if not Validators.validate_future_date(fecha):
                return {'error': 'La fecha debe ser futura'}, 400
            
            if not Validators.validate_business_hours(hora):
                return {'error': 'La hora debe estar entre 09:00 y 18:00'}, 400
            
            if not Validators.validate_service(data['Servicio']):
                return {'error': 'Servicio inválido'}, 400
            
            # Check availability
            if Reservacion.query.filter_by(Fecha=fecha, Hora=hora).first():
                return {'error': 'El horario ya está ocupado'}, 400
            
            # Validate NombrePersona if needed
            if data.get('ParaOtraPersona', False) and not data.get('NombrePersona', '').strip():
                return {'error': 'NombrePersona es requerido'}, 400
            
            # Create reservation
            nueva_reservacion = Reservacion(
                IdUser=data['IdUser'],
                Servicio=data['Servicio'].strip(),
                Fecha=fecha,
                Hora=hora,
                ParaOtraPersona=data.get('ParaOtraPersona', False),
                NombrePersona=data.get('NombrePersona', '').strip(),
                Estado=data.get('Estado', 'Pendiente')
            )
            
            db.session.add(nueva_reservacion)
            db.session.commit()
            logger.info(f"Reservación creada: ID {nueva_reservacion.IdReserva}")
            return nueva_reservacion.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear reservación: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def get_all_reservaciones():
        """Get all reservations"""
        try:
            reservaciones = Reservacion.query.all()
            return [r.to_dict() for r in reservaciones], 200
        except Exception as e:
            logger.error(f"Error al obtener reservaciones: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def update_reservacion(id, data):
        """Update a reservation"""
        try:
            reservacion = Reservacion.query.get(id)
            if not reservacion:
                return {'error': 'Reservación no encontrada'}, 404
            
            # Update fields with validation
            if 'Servicio' in data:
                if not Validators.validate_service(data['Servicio']):
                    return {'error': 'Servicio inválido'}, 400
                reservacion.Servicio = data['Servicio'].strip()
            
            if 'Fecha' in data:
                try:
                    fecha = datetime.strptime(data['Fecha'], '%Y-%m-%d').date()
                    if not Validators.validate_future_date(fecha):
                        return {'error': 'La fecha debe ser futura'}, 400
                    reservacion.Fecha = fecha
                except ValueError:
                    return {'error': 'Formato de fecha inválido'}, 400
            
            if 'Hora' in data:
                try:
                    hora = datetime.strptime(data['Hora'], '%H:%M').time()
                    if not Validators.validate_business_hours(hora):
                        return {'error': 'Hora fuera de horario laboral'}, 400
                    
                    # Check availability
                    fecha_check = reservacion.Fecha
                    if 'Fecha' in data:
                        fecha_check = datetime.strptime(data['Fecha'], '%Y-%m-%d').date()
                    
                    existing = Reservacion.query.filter_by(Fecha=fecha_check, Hora=hora)\
                        .filter(Reservacion.IdReserva != id).first()
                    if existing:
                        return {'error': 'El horario ya está ocupado'}, 400
                    
                    reservacion.Hora = hora
                except ValueError:
                    return {'error': 'Formato de hora inválido'}, 400
            
            if 'Estado' in data:
                if not Validators.validate_reservation_status(data['Estado']):
                    return {'error': 'Estado inválido'}, 400
                reservacion.Estado = data['Estado']
            
            if 'ParaOtraPersona' in data:
                reservacion.ParaOtraPersona = data['ParaOtraPersona']
            
            if 'NombrePersona' in data:
                if reservacion.ParaOtraPersona and not data['NombrePersona'].strip():
                    return {'error': 'NombrePersona es requerido'}, 400
                reservacion.NombrePersona = data['NombrePersona'].strip()
            
            db.session.commit()
            logger.info(f"Reservación actualizada: ID {id}")
            return reservacion.to_dict(), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar reservación: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500
    
    @staticmethod
    def delete_reservacion(id):
        """Delete a reservation"""
        try:
            reservacion = Reservacion.query.get(id)
            if not reservacion:
                return {'error': 'Reservación no encontrada'}, 404
            
            db.session.delete(reservacion)
            db.session.commit()
            logger.info(f"Reservación eliminada: ID {id}")
            return {'message': 'Reservación eliminada correctamente'}, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar reservación: {str(e)}")
            return {'error': 'Error interno del servidor'}, 500