from flask_restx import Namespace, Resource, fields
from flask import request
from src.services.auditoria_service import AuditoriaService
from src.utils.validators import Validators

login_auditoria_ns = Namespace('login-auditoria', description='Operaciones de auditoría')

auditoria_model = login_auditoria_ns.model('AuditoriaLogin', {
    'id': fields.Integer(readonly=True),
    'id_user': fields.Integer(),
    'usuario_ingresado': fields.String(required=True),
    'exito': fields.Boolean(required=True),
    'fecha': fields.String(readonly=True),
    'ip': fields.String(),
    'user_agent': fields.String()
})

@login_auditoria_ns.route('/')
class LoginAuditoriaList(Resource):
    @login_auditoria_ns.response(200, 'Lista de intentos')
    def get(self):
        """Obtener todos los intentos de login"""
        return AuditoriaService.get_all_logs()
    
    @login_auditoria_ns.expect(auditoria_model)
    @login_auditoria_ns.response(201, 'Intento registrado')
    def post(self):
        """Registrar un nuevo intento de login"""
        if not request.is_json:
            return {'error': 'El contenido debe ser application/json'}, 400
        
        data = request.get_json()
        required = ['usuario_ingresado', 'exito']
        missing, empty = Validators.validate_required_fields(data, required)
        
        if missing or empty:
            return {'error': 'Faltan campos requeridos'}, 400
        
        return AuditoriaService.create_log(data, request)

@login_auditoria_ns.route('/fallos')
class LoginAuditoriaFallos(Resource):
    @login_auditoria_ns.response(200, 'Lista de intentos fallidos')
    def get(self):
        """Obtener solo intentos fallidos"""
        return AuditoriaService.get_failed_logs()

@login_auditoria_ns.route('/hoy')
class LoginAuditoriaHoy(Resource):
    @login_auditoria_ns.response(200, 'Intentos del día actual')
    def get(self):
        """Obtener intentos del día"""
        return AuditoriaService.get_today_logs()