from extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    IdUser = db.Column('iduser', db.Integer, primary_key=True)
    Usuario = db.Column('usuario', db.String(100), unique=True, nullable=False)
    Nombre = db.Column('nombre', db.String(100), nullable=False)
    Apellido = db.Column('apellido', db.String(100), nullable=False)
    Email = db.Column('email', db.String(250), unique=True, nullable=False)
    Telefono = db.Column('telefono', db.String(10))
    Passsword = db.Column('passsword', db.String(100), nullable=False)

    reservaciones = db.relationship('Reservacion', backref='usuario_ref', lazy=True)

    def to_dict(self):
        return {
            'IdUser': self.IdUser,
            'Usuario': self.Usuario,
            'Nombre': self.Nombre,
            'Apellido': self.Apellido,
            'Email': self.Email,
            'Telefono': self.Telefono,
            'Passsword': self.Passsword
        }