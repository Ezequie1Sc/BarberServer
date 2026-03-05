from extensions import db
from src.utils.helpers import serialize_datetime

class AuditoriaLogin(db.Model):
    __tablename__ = 'auditoria_logins'
    
    id = db.Column('id', db.Integer, primary_key=True)
    id_user = db.Column('id_user', db.Integer, db.ForeignKey('usuarios.iduser'))
    usuario_ingresado = db.Column('usuario_ingresado', db.String(100), nullable=False)
    exito = db.Column('exito', db.Boolean, nullable=False)
    fecha = db.Column('fecha', db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    ip = db.Column('ip', db.String(50))
    user_agent = db.Column('user_agent', db.String(250))

    def to_dict(self):
        return {
            'id': self.id,
            'id_user': self.id_user,
            'usuario_ingresado': self.usuario_ingresado,
            'exito': self.exito,
            'fecha': serialize_datetime(self.fecha),
            'ip': self.ip,
            'user_agent': self.user_agent
        }