#!/usr/bin/env python3
"""
Script para migrar la base de datos y agregar la columna de portada
"""

from main import app, db
from sqlalchemy import text

def agregar_columna_portada():
    with app.app_context():
        try:
            # Verificar si la columna portada ya existe
            result = db.session.execute(text("PRAGMA table_info(libros)"))
            columnas = [row[1] for row in result.fetchall()]
            
            if 'portada' not in columnas:
                print("Agregando columna 'portada' a la tabla libros...")
                db.session.execute(text("ALTER TABLE libros ADD COLUMN portada VARCHAR(255)"))
                db.session.commit()
                print("Columna 'portada' agregada exitosamente")
            else:
                print("La columna 'portada' ya existe en la tabla libros")
                
        except Exception as e:
            print(f"Error al agregar la columna portada: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    agregar_columna_portada() 