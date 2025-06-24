#!/usr/bin/env python3
"""
Script para migrar la base de datos y agregar la tabla de miembros
"""

from main import app, db
from models import Miembro

def migrate_miembros():
    """Migra la base de datos para agregar la tabla de miembros"""
    with app.app_context():
        try:
            # Crear la tabla de miembros
            db.create_all()
            print("✅ Tabla de miembros creada exitosamente")
            
            # Verificar si la tabla se creó correctamente
            try:
                # Intentar hacer una consulta simple para verificar que la tabla existe
                count = Miembro.query.count()
                print(f"✅ Tabla de miembros verificada. Miembros actuales: {count}")
            except Exception as e:
                print(f"❌ Error al verificar la tabla: {str(e)}")
                return False
            
            print("🎉 Migración completada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            return False

if __name__ == "__main__":
    print("🔄 Iniciando migración de la tabla de miembros...")
    success = migrate_miembros()
    
    if success:
        print("\n✅ La migración se completó exitosamente.")
        print("📋 Ahora puedes:")
        print("   - Acceder a la gestión de miembros desde el menú de administración")
        print("   - Registrar nuevos miembros")
        print("   - Generar carnets imprimibles")
    else:
        print("\n❌ La migración falló. Revisa los errores anteriores.") 