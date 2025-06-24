#!/usr/bin/env python3
"""
Script para migrar la base de datos y agregar el campo email a la tabla de miembros
"""

from main import app, db
from models import Miembro
import sqlite3

def agregar_columna_email():
    """Agrega la columna email a la tabla miembros si no existe"""
    try:
        with app.app_context():
            # Conectar directamente a la base de datos SQLite
            conn = sqlite3.connect('instance/biblioteca.db')
            cursor = conn.cursor()
            
            # Verificar si la columna email ya existe
            cursor.execute("PRAGMA table_info(miembros)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            if 'email' not in columnas:
                print("Agregando columna email a la tabla miembros...")
                cursor.execute("ALTER TABLE miembros ADD COLUMN email TEXT")
                
                # Actualizar registros existentes con un email temporal
                cursor.execute("UPDATE miembros SET email = 'sin_email@biblioteca.com' WHERE email IS NULL")
                
                conn.commit()
                print("Columna email agregada exitosamente")
            else:
                print("La columna email ya existe en la tabla miembros")
            
            conn.close()
            
    except Exception as e:
        print(f"Error al agregar columna email: {str(e)}")

if __name__ == '__main__':
    agregar_columna_email()

def migrate_email_miembros():
    """Migra la base de datos para agregar el campo email a la tabla de miembros"""
    with app.app_context():
        try:
            # Conectar directamente a SQLite para agregar la columna
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            
            # Verificar si la columna email ya existe
            cursor.execute("PRAGMA table_info(miembros)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'email' not in columns:
                # Agregar la columna email
                cursor.execute("ALTER TABLE miembros ADD COLUMN email VARCHAR(120)")
                print("✅ Columna email agregada exitosamente")
                
                # Actualizar miembros existentes con un email temporal
                cursor.execute("SELECT id, nombres, apellidos FROM miembros WHERE email IS NULL")
                miembros_sin_email = cursor.fetchall()
                
                for miembro_id, nombres, apellidos in miembros_sin_email:
                    email_temporal = f"{nombres.lower().replace(' ', '')}.{apellidos.lower().replace(' ', '')}@biblioteca.com"
                    cursor.execute("UPDATE miembros SET email = ? WHERE id = ?", (email_temporal, miembro_id))
                    print(f"✅ Email temporal asignado a {nombres} {apellidos}: {email_temporal}")
                
                conn.commit()
                print(f"✅ Se actualizaron {len(miembros_sin_email)} miembros con email temporal")
            else:
                print("ℹ️  La columna email ya existe")
            
            conn.close()
            
            # Verificar que todo funciona correctamente
            miembros = Miembro.query.all()
            print(f"✅ Verificación completada. Total de miembros: {len(miembros)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            return False

if __name__ == "__main__":
    print("🔄 Iniciando migración para agregar campo email...")
    success = migrate_email_miembros()
    
    if success:
        print("\n✅ La migración se completó exitosamente.")
        print("📋 Ahora puedes:")
        print("   - Registrar miembros con correo electrónico")
        print("   - Buscar miembros por email")
        print("   - Editar el email de miembros existentes")
        print("   - Los miembros existentes tienen un email temporal asignado")
    else:
        print("\n❌ La migración falló. Revisa los errores anteriores.") 