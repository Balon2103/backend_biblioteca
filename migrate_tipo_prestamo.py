#!/usr/bin/env python3
"""
Script para migrar la base de datos y agregar campos para tipo de préstamo
"""

from main import app, db
from models import PersonaPrestamo
import sqlite3

def migrar_tipo_prestamo():
    with app.app_context():
        try:
            # Verificar si la columna tipo_prestamo existe
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            
            # Obtener información de las columnas de la tabla personas_prestamo
            cursor.execute("PRAGMA table_info(personas_prestamo)")
            columns = [column[1] for column in cursor.fetchall()]
            
            print("Columnas existentes en personas_prestamo:", columns)
            
            # Agregar columnas si no existen
            if 'tipo_prestamo' not in columns:
                print("Agregando columna tipo_prestamo...")
                cursor.execute("ALTER TABLE personas_prestamo ADD COLUMN tipo_prestamo TEXT DEFAULT 'externo'")
                print("Columna tipo_prestamo agregada")
            
            if 'institucion' not in columns:
                print("Agregando columna institucion...")
                cursor.execute("ALTER TABLE personas_prestamo ADD COLUMN institucion TEXT")
                print("Columna institucion agregada")
            
            if 'cargo' not in columns:
                print("Agregando columna cargo...")
                cursor.execute("ALTER TABLE personas_prestamo ADD COLUMN cargo TEXT")
                print("Columna cargo agregada")
            
            # Actualizar registros existentes
            print("Actualizando registros existentes...")
            cursor.execute("UPDATE personas_prestamo SET tipo_prestamo = 'externo' WHERE tipo_prestamo IS NULL")
            
            conn.commit()
            conn.close()
            
            print("Migración completada exitosamente")
            
            # Verificar los cambios
            prestamos = PersonaPrestamo.query.all()
            print(f"Total de préstamos externos: {len(prestamos)}")
            for prestamo in prestamos[:5]:  # Mostrar los primeros 5
                print(f"- {prestamo.nombre} {prestamo.apellido}: {prestamo.tipo_prestamo}")
            
        except Exception as e:
            print(f"Error en la migración: {str(e)}")

if __name__ == '__main__':
    migrar_tipo_prestamo() 