import pandas as pd
from flask import Flask
from extensions import db
from models import Libro
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Mapea aquí los nombres de las columnas del Excel a los campos del modelo Libro
COLUMN_MAP = {
    'titulo': 'titulo',
    'autor': 'autor',
    'cota': 'cota',
    'verificacion': 'verificacion',
    'anio_edicion': 'anio_edicion',
    'medidas': 'medidas',
    'num_paginas': 'num_paginas',
    'ciudad': 'ciudad',
    'editorial': 'editorial',
    'coleccion': 'coleccion',
    'materias': 'materias',
    'caract_formato': 'caract_formato',
    'cant_ejemplares': 'cant_ejemplares',
    'tomos': 'tomos',
}

with app.app_context():
    # Leer el archivo Excel
    df = pd.read_excel('Inventario Bibliografico.xlsx')
    print(f"Columnas encontradas en el Excel: {list(df.columns)}")

    # Renombrar columnas según el modelo
    df = df.rename(columns={col: COLUMN_MAP[col] for col in df.columns if col in COLUMN_MAP})

    # Rellenar NaN con string vacío
    df = df.fillna('')

    # Insertar libros
    count = 0
    for _, row in df.iterrows():
        libro = Libro(**{field: row.get(field, '') for field in COLUMN_MAP.values()})
        db.session.add(libro)
        count += 1
    db.session.commit()
    print(f"Se importaron {count} libros correctamente desde el Excel.") 