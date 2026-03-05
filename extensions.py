from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()
api = Api(
    version='1.0',
    title='API de Barbería',
    description='API para gestión de usuarios, reservaciones y auditoría'
)