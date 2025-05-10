from flask import Flask
from extensions import db
from models import Libro
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Leer el archivo JSON
    with open('libros.json', 'r', encoding='utf-8') as f:
        libros_data = json.load(f)
    
    # Verificar si ya existen libros
    if Libro.query.count() == 0:
        for libro_data in libros_data:
            libro = Libro(**libro_data)
            db.session.add(libro)
        db.session.commit()
        print(f"Se importaron {len(libros_data)} libros correctamente")
    else:
        print("Ya existen libros en la base de datos") 