from extensions import db
from src.utils.helpers import serialize_datetime

class Reservacion(db.Model):
    __tablename__ = 'reservaciones'
    
    IdReserva = db.Column('idreserva', db.Integer, primary_key=True)
    IdUser = db.Column('iduser', db.Integer, db.ForeignKey('usuarios.iduser'), nullable=False)
    Servicio = db.Column('servicio', db.String(100), nullable=False)
    Fecha = db.Column('fecha', db.Date, nullable=False)
    Hora = db.Column('hora', db.Time, nullable=False)
    ParaOtraPersona = db.Column('paraotrapersona', db.Boolean, nullable=False, default=False)
    NombrePersona = db.Column('nombrepersona', db.String(100))
    Estado = db.Column('estado', db.String(50), nullable=False, default='Pendiente')
    FechaCreacion = db.Column('fechacreacion', db.TIMESTAMP, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'IdReserva': self.IdReserva,
            'IdUser': self.IdUser,
            'Servicio': self.Servicio,
            'Fecha': serialize_datetime(self.Fecha),
            'Hora': serialize_datetime(self.Hora),
            'ParaOtraPersona': self.ParaOtraPersona,
            'NombrePersona': self.NombrePersona,
            'Estado': self.Estado,
            'FechaCreacion': serialize_datetime(self.FechaCreacion)
        }