from flask_restx import Namespace, Resource, fields
from flask import request
from src.services.reservacion_service import ReservacionService
from src.utils.validators import Validators

reservaciones_ns = Namespace('reservaciones', description='Operaciones con reservaciones')

reservacion_model = reservaciones_ns.model('Reservacion', {
    'IdReserva': fields.Integer(readonly=True, description='ID de la reservación'),
    'IdUser': fields.Integer(required=True, description='ID del usuario'),
    'Servicio': fields.String(required=True, description='Tipo de servicio'),
    'Fecha': fields.String(required=True, description='Fecha (YYYY-MM-DD)'),
    'Hora': fields.String(required=True, description='Hora (HH:MM)'),
    'ParaOtraPersona': fields.Boolean(default=False),
    'NombrePersona': fields.String(description='Nombre de la persona'),
    'Estado': fields.String(default='Pendiente'),
    'FechaCreacion': fields.String(readonly=True)
})

@reservaciones_ns.route('/')
class ReservacionList(Resource):
    @reservaciones_ns.expect(reservacion_model)
    @reservaciones_ns.response(201, 'Reservación creada')
    @reservaciones_ns.response(400, 'Validación fallida')
    def post(self):
        """Crear una nueva reservación"""
        if not request.is_json:
            return {'error': 'El contenido debe ser application/json'}, 400
        
        data = request.get_json()
        required = ['IdUser', 'Servicio', 'Fecha', 'Hora']
        missing, empty = Validators.validate_required_fields(data, required)
        
        if missing or empty:
            return {'error': 'Faltan campos requeridos'}, 400
        
        return ReservacionService.create_reservacion(data)
    
    @reservaciones_ns.response(200, 'Lista de reservaciones')
    def get(self):
        """Listar todas las reservaciones"""
        return ReservacionService.get_all_reservaciones()

@reservaciones_ns.route('/<int:id>')
class ReservacionResource(Resource):
    @reservaciones_ns.expect(reservacion_model)
    @reservaciones_ns.response(200, 'Reservación actualizada')
    @reservaciones_ns.response(404, 'Reservación no encontrada')
    def put(self, id):
        """Actualizar una reservación"""
        if not request.is_json:
            return {'error': 'El contenido debe ser application/json'}, 400
        
        return ReservacionService.update_reservacion(id, request.get_json())
    
    @reservaciones_ns.response(200, 'Reservación eliminada')
    @reservaciones_ns.response(404, 'Reservación no encontrada')
    def delete(self, id):
        """Eliminar una reservación"""
        return ReservacionService.delete_reservacion(id)