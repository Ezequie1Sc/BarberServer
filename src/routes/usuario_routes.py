from flask_restx import Namespace, Resource, fields
from flask import request
from src.services.usuario_service import UsuarioService
from src.utils.validators import Validators

usuarios_ns = Namespace('usuarios', description='Operaciones con usuarios')

# Modelos para la API
usuario_model = usuarios_ns.model('Usuario', {
    'IdUser': fields.Integer(readonly=True, description='Identificador único'),
    'Usuario': fields.String(required=True, description='Nombre de usuario'),
    'Nombre': fields.String(required=True, description='Nombre real'),
    'Apellido': fields.String(required=True, description='Apellido'),
    'Email': fields.String(required=True, description='Correo electrónico'),
    'Telefono': fields.String(description='Teléfono de contacto'),
    'Passsword': fields.String(required=True, description='Contraseña')
})

login_model = usuarios_ns.model('Login', {
    'Usuario': fields.String(required=True, description='Nombre de usuario'),
    'Passsword': fields.String(required=True, description='Contraseña')
})

@usuarios_ns.route('/')
class UsuarioList(Resource):
    @usuarios_ns.expect(usuario_model)
    @usuarios_ns.response(201, 'Usuario creado')
    @usuarios_ns.response(400, 'Validación fallida')
    @usuarios_ns.response(500, 'Error interno')
    def post(self):
        """Crear un nuevo usuario"""
        if not request.is_json:
            return {'error': 'El contenido debe ser application/json'}, 400
        
        data = request.get_json()
        
        # Validate required fields
        required = ['Usuario', 'Nombre', 'Apellido', 'Email', 'Passsword']
        missing, empty = Validators.validate_required_fields(data, required)
        
        if missing:
            return {'error': 'Faltan campos', 'campos_faltantes': missing}, 400
        
        if empty:
            return {'error': 'Campos vacíos', 'campos_vacios': empty}, 400
        
        # Validate email
        if not Validators.validate_email(data['Email']):
            return {'error': 'Formato de email inválido'}, 400
        
        return UsuarioService.create_usuario(data)
    
    @usuarios_ns.response(200, 'Lista de usuarios')
    def get(self):
        """Listar todos los usuarios"""
        return UsuarioService.get_all_usuarios()

@usuarios_ns.route('/<int:id>')
class UsuarioResource(Resource):
    @usuarios_ns.expect(usuario_model)
    @usuarios_ns.response(200, 'Usuario actualizado')
    @usuarios_ns.response(404, 'Usuario no encontrado')
    def put(self, id):
        """Actualizar un usuario"""
        if not request.is_json:
            return {'error': 'El contenido debe ser application/json'}, 400
        
        return UsuarioService.update_usuario(id, request.get_json())
    
    @usuarios_ns.response(200, 'Usuario eliminado')
    @usuarios_ns.response(404, 'Usuario no encontrado')
    def delete(self, id):
        """Eliminar un usuario"""
        return UsuarioService.delete_usuario(id)

@usuarios_ns.route('/login')
class UsuarioLogin(Resource):
    @usuarios_ns.expect(login_model)
    @usuarios_ns.response(200, 'Login exitoso')
    @usuarios_ns.response(401, 'Credenciales inválidas')
    def post(self):
        """Autenticar usuario"""
        if not request.is_json:
            return {'error': 'El contenido debe ser application/json'}, 400
        
        data = request.get_json()
        required = ['Usuario', 'Passsword']
        missing, empty = Validators.validate_required_fields(data, required)
        
        if missing or empty:
            return {'error': 'Usuario y contraseña requeridos'}, 400
        
        return UsuarioService.login(data, request)