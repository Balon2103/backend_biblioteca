#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corregir la migración y hacer miembro_id nullable
"""

import sqlite3
import os

DB_PATH = "biblioteca.db"

def corregir_migracion():
    if not os.path.exists(DB_PATH):
        print(f"Error: No se encuentra la base de datos {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        print("=== CORRIGIENDO MIGRACIÓN ===")
        print("Desactivando claves foráneas temporalmente...")
        c.execute("PRAGMA foreign_keys=off;")
        
        print("Renombrando tabla original...")
        c.execute("ALTER TABLE prestamos_internos RENAME TO prestamos_internos_old;")
        
        print("Creando nueva tabla con miembro_id NULLABLE...")
        c.execute('''
        CREATE TABLE prestamos_internos (
            id INTEGER PRIMARY KEY,
            miembro_id INTEGER,
            libro_id INTEGER NOT NULL,
            fecha_prestamo DATETIME NOT NULL,
            fecha_devolucion_esperada DATETIME NOT NULL,
            fecha_devolucion_real DATETIME,
            estado VARCHAR(20) DEFAULT 'activo',
            FOREIGN KEY(libro_id) REFERENCES libros(id),
            FOREIGN KEY(miembro_id) REFERENCES miembros(id) ON DELETE SET NULL
        );
        ''')
        
        print("Copiando datos...")
        c.execute('''
        INSERT INTO prestamos_internos (id, miembro_id, libro_id, fecha_prestamo, fecha_devolucion_esperada, fecha_devolucion_real, estado)
        SELECT id, miembro_id, libro_id, fecha_prestamo, fecha_devolucion_esperada, fecha_devolucion_real, estado
        FROM prestamos_internos_old;
        ''')
        
        print("Eliminando tabla antigua...")
        c.execute("DROP TABLE prestamos_internos_old;")
        
        print("Reactivando claves foráneas...")
        c.execute("PRAGMA foreign_keys=on;")
        
        conn.commit()
        print("✅ Migración corregida con éxito!")
        
        # Verificar que los datos se copiaron correctamente
        c.execute("SELECT COUNT(*) FROM prestamos_internos;")
        count = c.fetchone()[0]
        print(f"Total de préstamos internos: {count}")
        
        # Verificar estructura
        c.execute("PRAGMA table_info(prestamos_internos);")
        columns = c.fetchall()
        print("\nEstructura corregida:")
        for col in columns:
            print(f"   {col[1]} {col[2]} {'NULL' if col[3] else 'NOT NULL'}")
        
    except Exception as e:
        print(f"❌ Error durante la corrección: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    corregir_migracion() 