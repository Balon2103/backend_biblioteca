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
    'Título ': 'titulo',
    'Autor': 'autor',
    'COTA': 'cota',
    'Verificación': 'verificacion',
    'Año de edicion ': 'anio_edicion',
    'Medidas ': 'medidas',
    'Num. Paginas': 'num_paginas',
    'Ciudad': 'ciudad',
    'Editorial': 'editorial',
    'Colección ': 'coleccion',
    'Materias': 'materias',
    'Caract.Formato ': 'caract_formato',
    'Cant. Ejemplares': 'cant_ejemplares',
    'Tomos': 'tomos',
}

with app.app_context():
    # Borrar todos los libros existentes antes de importar
    print("Eliminando libros existentes...")
    Libro.query.delete()
    db.session.commit()

    # Leer el archivo Excel
    df = pd.read_excel('Inventario Bibliografico.xlsx')
    print(f"Columnas encontradas en el Excel: {list(df.columns)}")

    # Renombrar columnas según el modelo
    df = df.rename(columns={col: COLUMN_MAP[col] for col in df.columns if col in COLUMN_MAP})

    # Rellenar NaN con string vacío
    df = df.fillna('')

    # Filtrar solo filas con título no vacío
    df = df[df['titulo'].str.strip() != '']

    # Mostrar una muestra de los datos a importar
    print("Ejemplo de libros a importar:")
    print(df.head(5).to_dict(orient='records'))

    # Insertar libros
    count = 0
    for _, row in df.iterrows():
        libro = Libro(**{field: row.get(field, '') for field in COLUMN_MAP.values()})
        db.session.add(libro)
        count += 1
    db.session.commit()
    print(f"Se importaron {count} libros correctamente desde el Excel.") 