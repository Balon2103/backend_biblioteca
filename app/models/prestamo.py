from app import db
from datetime import datetime

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')
    
    def marcar_como_devuelto(self):
        self.fecha_devolucion_real = datetime.utcnow()
        self.estado = 'devuelto'
        self.libro.disponible = True
    
    def __repr__(self):
        return f'<Prestamo {self.id}>'

class PersonaPrestamo(db.Model):
    __tablename__ = 'persona_prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    observaciones = db.Column(db.Text)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')
    
    def marcar_como_devuelto(self):
        self.fecha_devolucion_real = datetime.utcnow()
        self.estado = 'devuelto'
        self.libro.disponible = True
    
    def __repr__(self):
        return f'<PersonaPrestamo {self.id}>' 