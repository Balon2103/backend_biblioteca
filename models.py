from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    rol = db.Column(db.String(20), default='usuario')  # 'usuario', 'admin', 'superadmin'
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    cedula = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.String(20))
    prestamos = db.relationship('Prestamo', backref='usuario', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt='password-reset-salt')
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='password-reset-salt', max_age=expires_sec)
            return Usuario.query.filter_by(email=email).first()
        except:
            return None
            
    @property
    def is_superadmin(self):
        return self.rol == 'superadmin'

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    autor = db.Column(db.String(200))
    cota = db.Column(db.String(50))
    verificacion = db.Column(db.String(50))
    anio_edicion = db.Column(db.String(20))
    medidas = db.Column(db.String(50))
    num_paginas = db.Column(db.String(20))
    ciudad = db.Column(db.String(100))
    editorial = db.Column(db.String(200))
    coleccion = db.Column(db.String(200))
    materias = db.Column(db.Text)
    caract_formato = db.Column(db.String(100))
    cant_ejemplares = db.Column(db.String(20))
    tomos = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)
    portada = db.Column(db.String(255))  # Ruta de la imagen de portada
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)

    def __repr__(self):
        return f'<Libro {self.titulo}>'

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')  # activo, devuelto, vencido
    
    def __repr__(self):
        return f'<Prestamo {self.id}>'

class PersonaPrestamo(db.Model):
    __tablename__ = 'personas_prestamo'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    tipo_prestamo = db.Column(db.String(20), default='externo')  # externo
    institucion = db.Column(db.String(200))  # Para préstamos externos
    cargo = db.Column(db.String(100))  # Para préstamos externos
    observaciones = db.Column(db.Text)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')  # activo, devuelto, vencido
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    libro = db.relationship('Libro', backref=db.backref('personas_prestamo', lazy=True))
    
    def __repr__(self):
        return f'<PersonaPrestamo {self.id}>'
        
    @property
    def esta_vencido(self):
        if self.estado == 'activo' and datetime.utcnow() > self.fecha_devolucion_esperada:
            return True
        return False
        
    def marcar_como_devuelto(self):
        self.estado = 'devuelto'
        self.fecha_devolucion_real = datetime.utcnow()
        self.libro.disponible = True
    
    @property
    def tipo_prestamo_display(self):
        """Retorna el nombre legible del tipo de préstamo"""
        tipos = {
            'externo': 'Préstamo Externo'
        }
        return tipos.get(self.tipo_prestamo, self.tipo_prestamo)

class Miembro(db.Model):
    __tablename__ = 'miembros'
    
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    foto = db.Column(db.String(255))  # Ruta de la imagen
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activo')  # activo, inactivo, suspendido
    numero_carnet = db.Column(db.String(20), unique=True)
    
    def __repr__(self):
        return f'<Miembro {self.nombres} {self.apellidos}>'
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    def generar_numero_carnet(self):
        """Genera un número de carnet único basado en el año y un contador"""
        from datetime import datetime
        año_actual = datetime.now().year
        # Contar miembros existentes para este año
        miembros_año = Miembro.query.filter(
            Miembro.numero_carnet.like(f'{año_actual}%')
        ).count()
        return f"{año_actual}{str(miembros_año + 1).zfill(4)}"

class PrestamoInterno(db.Model):
    __tablename__ = 'prestamos_internos'
    
    id = db.Column(db.Integer, primary_key=True)
    miembro_id = db.Column(db.Integer, db.ForeignKey('miembros.id', ondelete='SET NULL'), nullable=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')  # activo, devuelto, vencido
    libro = db.relationship('Libro', backref=db.backref('prestamos_internos', lazy=True))
    miembro = db.relationship('Miembro', backref=db.backref('prestamos_internos', lazy=True), passive_deletes=True)
    
    def __repr__(self):
        return f'<PrestamoInterno {self.id}>'
    
    @property
    def esta_vencido(self):
        if self.estado == 'activo' and datetime.utcnow() > self.fecha_devolucion_esperada:
            return True
        return False
        
    def marcar_como_devuelto(self):
        self.estado = 'devuelto'
        self.fecha_devolucion_real = datetime.utcnow()
        self.libro.disponible = True
