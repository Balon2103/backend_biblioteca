from app import db

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200))
    cota = db.Column(db.String(50))
    editorial = db.Column(db.String(200))
    anio_edicion = db.Column(db.String(4))
    ciudad = db.Column(db.String(100))
    coleccion = db.Column(db.String(200))
    medidas = db.Column(db.String(50))
    num_paginas = db.Column(db.Integer)
    caract_formato = db.Column(db.String(100))
    cant_ejemplares = db.Column(db.Integer)
    tomos = db.Column(db.String(50))
    verificacion = db.Column(db.String(50))
    materias = db.Column(db.String(200))
    disponible = db.Column(db.Boolean, default=True)

    # ✅ Nuevo campo para múltiples portadas (sin warning)
    portadas = db.Column(db.JSON, default=list)

    # Relaciones
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)
    prestamos_externos = db.relationship('PersonaPrestamo', backref='libro', lazy=True)
    
    def __repr__(self):
        return f'<Libro {self.titulo}>'
