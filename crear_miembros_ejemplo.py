#!/usr/bin/env python3
"""
Script para crear miembros de ejemplo en la base de datos
"""

from main import app, db
from models import Miembro
from datetime import datetime

def crear_miembros_ejemplo():
    """Crea algunos miembros de ejemplo"""
    with app.app_context():
        try:
            # Verificar si ya existen miembros
            if Miembro.query.count() > 0:
                print("⚠️  Ya existen miembros en la base de datos. Saltando creación de ejemplos.")
                return True
            
            # Lista de miembros de ejemplo
            miembros_ejemplo = [
                {
                    'nombres': 'Juan Carlos',
                    'apellidos': 'González Pérez',
                    'cedula': '1234567890',
                    'telefono': '0412-123-4567',
                    'direccion': 'Av. Principal, Edificio Los Rosales, Apto 5B, Caracas'
                },
                {
                    'nombres': 'María Elena',
                    'apellidos': 'Rodríguez Silva',
                    'cedula': '0987654321',
                    'telefono': '0424-987-6543',
                    'direccion': 'Calle Bolívar #123, Sector Centro, Valencia'
                },
                {
                    'nombres': 'Carlos Alberto',
                    'apellidos': 'Martínez López',
                    'cedula': '1122334455',
                    'telefono': '0416-555-1234',
                    'direccion': 'Urbanización El Bosque, Casa 15, Maracay'
                },
                {
                    'nombres': 'Ana Sofía',
                    'apellidos': 'Hernández Torres',
                    'cedula': '5566778899',
                    'telefono': '0426-777-8888',
                    'direccion': 'Residencial Los Pinos, Torre A, Piso 8, Apto 8A, Barquisimeto'
                },
                {
                    'nombres': 'Luis Fernando',
                    'apellidos': 'Díaz Mendoza',
                    'cedula': '9988776655',
                    'telefono': '0414-333-2222',
                    'direccion': 'Sector La Viña, Calle 5, Casa 25, Mérida'
                }
            ]
            
            # Crear los miembros
            for i, datos in enumerate(miembros_ejemplo, 1):
                miembro = Miembro(
                    nombres=datos['nombres'],
                    apellidos=datos['apellidos'],
                    cedula=datos['cedula'],
                    telefono=datos['telefono'],
                    direccion=datos['direccion'],
                    fecha_registro=datetime.utcnow()
                )
                
                # Generar número de carnet
                miembro.numero_carnet = miembro.generar_numero_carnet()
                
                db.session.add(miembro)
                print(f"✅ Miembro {i} creado: {miembro.nombre_completo} - Carnet: {miembro.numero_carnet}")
            
            # Guardar todos los cambios
            db.session.commit()
            print(f"\n🎉 Se crearon {len(miembros_ejemplo)} miembros de ejemplo exitosamente")
            
            # Mostrar resumen
            total_miembros = Miembro.query.count()
            print(f"📊 Total de miembros en la base de datos: {total_miembros}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear miembros de ejemplo: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🔄 Creando miembros de ejemplo...")
    success = crear_miembros_ejemplo()
    
    if success:
        print("\n✅ Los miembros de ejemplo se crearon correctamente.")
        print("📋 Ahora puedes:")
        print("   - Iniciar la aplicación con: python main.py")
        print("   - Acceder a la gestión de miembros")
        print("   - Ver los miembros creados")
        print("   - Generar carnets para cada miembro")
    else:
        print("\n❌ Error al crear los miembros de ejemplo.") 