from flask import Flask
from extensions import db
from models import Libro
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    libros = Libro.query.all()
    libros_data = []
    for libro in libros:
        libro_dict = {
            'titulo': libro.titulo,
            'autor': libro.autor,
            'cota': libro.cota,
            'editorial': libro.editorial,
            'anio_edicion': libro.anio_edicion,
            'ciudad': libro.ciudad,
            'coleccion': libro.coleccion,
            'medidas': libro.medidas,
            'num_paginas': libro.num_paginas,
            'caract_formato': libro.caract_formato,
            'cant_ejemplares': libro.cant_ejemplares,
            'tomos': libro.tomos,
            'verificacion': libro.verificacion,
            'materias': libro.materias,
            'disponible': libro.disponible
        }
        libros_data.append(libro_dict)
    
    with open('libros.json', 'w', encoding='utf-8') as f:
        json.dump(libros_data, f, ensure_ascii=False, indent=2)
    
    print(f"Se exportaron {len(libros_data)} libros a libros.json") 