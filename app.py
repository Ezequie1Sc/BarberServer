from flask import Flask, jsonify
from flask_restx import Resource
from sqlalchemy import text
from config import Config
from extensions import db, cors, api
from src.utils.helpers import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup logging
    logger = setup_logging(app)
    
    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    api.init_app(app)
    
    # Import and register namespaces
    from src.routes.usuario_routes import usuarios_ns
    from src.routes.reservacion_routes import reservaciones_ns
    from src.routes.auditoria_routes import login_auditoria_ns
    
    api.add_namespace(usuarios_ns, path='/usuarios')
    api.add_namespace(reservaciones_ns, path='/reservaciones')
    api.add_namespace(login_auditoria_ns, path='/login-auditoria')
    
    # Health check endpoint
    @app.route('/healthcheck')
    def healthcheck():
        try:
            db.session.execute(text('SELECT 1'))
            return {'status': 'OK', 'database': 'connected'}, 200
        except Exception as e:
            logger.error(f"Error de healthcheck: {str(e)}")
            return {'status': 'Error', 'message': str(e)}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print("✅ Conexión a la base de datos exitosa")
        except Exception as e:
            print(f"❌ Error de conexión a la base de datos: {str(e)}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)