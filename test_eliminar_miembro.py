#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba para verificar la eliminación de miembros
"""

import os
import sys
from main import app, db
from models import Miembro, PrestamoInterno

def test_eliminar_miembro():
    """Prueba la eliminación de un miembro"""
    
    with app.app_context():
        print("=== PRUEBA DE ELIMINACIÓN DE MIEMBROS ===")
        
        # 1. Verificar si hay miembros en la base de datos
        total_miembros = Miembro.query.count()
        print(f"Total de miembros en la base de datos: {total_miembros}")
        
        if total_miembros == 0:
            print("No hay miembros para probar. Creando un miembro de prueba...")
            
            # Crear un miembro de prueba
            miembro_prueba = Miembro(
                nombres="Juan",
                apellidos="Pérez",
                cedula="12345678",
                email="juan.perez@test.com",
                telefono="123456789",
                direccion="Dirección de prueba",
                numero_carnet="TEST001",
                estado="activo"
            )
            db.session.add(miembro_prueba)
            db.session.commit()
            print(f"Miembro de prueba creado con ID: {miembro_prueba.id}")
        
        # 2. Obtener el primer miembro
        miembro = Miembro.query.first()
        if not miembro:
            print("No se pudo obtener ningún miembro")
            return
        
        print(f"\nMiembro a eliminar:")
        print(f"  ID: {miembro.id}")
        print(f"  Nombre: {miembro.nombre_completo}")
        print(f"  Cédula: {miembro.cedula}")
        
        # 3. Verificar si tiene préstamos asociados
        prestamos_count = PrestamoInterno.query.filter_by(miembro_id=miembro.id).count()
        print(f"  Préstamos asociados: {prestamos_count}")
        
        if prestamos_count > 0:
            print("\n⚠️  El miembro tiene préstamos asociados. No se puede eliminar.")
            print("Préstamos encontrados:")
            
            prestamos = PrestamoInterno.query.filter_by(miembro_id=miembro.id).all()
            for prestamo in prestamos:
                print(f"  - Préstamo ID: {prestamo.id}, Estado: {prestamo.estado}")
                if prestamo.libro:
                    print(f"    Libro: {prestamo.libro.titulo}")
            
            print("\nPara eliminar este miembro, primero debe:")
            print("1. Ir a la vista de préstamos del miembro")
            print("2. Devolver todos los préstamos activos")
            print("3. Luego intentar eliminar el miembro")
            
        else:
            print("\n✅ El miembro no tiene préstamos asociados. Se puede eliminar.")
            
            # 4. Intentar eliminar el miembro
            try:
                print("Intentando eliminar el miembro...")
                
                # Verificar si tiene foto
                if miembro.foto:
                    foto_path = os.path.join(app.static_folder, miembro.foto)
                    if os.path.exists(foto_path):
                        print(f"Eliminando foto: {foto_path}")
                        os.remove(foto_path)
                
                # Eliminar de la base de datos
                db.session.delete(miembro)
                db.session.commit()
                
                print("✅ Miembro eliminado exitosamente")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error al eliminar miembro: {str(e)}")
                print(f"Tipo de error: {type(e).__name__}")
        
        # 5. Verificar el estado final
        miembro_restante = Miembro.query.filter_by(id=miembro.id).first()
        if miembro_restante:
            print(f"\n⚠️  El miembro aún existe en la base de datos (ID: {miembro_restante.id})")
        else:
            print(f"\n✅ El miembro fue eliminado correctamente de la base de datos")

def verificar_integridad():
    """Verifica la integridad de la base de datos"""
    
    with app.app_context():
        print("\n=== VERIFICACIÓN DE INTEGRIDAD ===")
        
        # Verificar miembros sin préstamos
        miembros_sin_prestamos = []
        for miembro in Miembro.query.all():
            prestamos_count = PrestamoInterno.query.filter_by(miembro_id=miembro.id).count()
            if prestamos_count == 0:
                miembros_sin_prestamos.append(miembro)
        
        print(f"Miembros sin préstamos: {len(miembros_sin_prestamos)}")
        for miembro in miembros_sin_prestamos:
            print(f"  - {miembro.nombre_completo} (ID: {miembro.id})")
        
        # Verificar préstamos huérfanos
        prestamos_huérfanos = []
        for prestamo in PrestamoInterno.query.all():
            miembro = Miembro.query.get(prestamo.miembro_id)
            if not miembro:
                prestamos_huérfanos.append(prestamo)
        
        print(f"Préstamos huérfanos: {len(prestamos_huérfanos)}")
        for prestamo in prestamos_huérfanos:
            print(f"  - Préstamo ID: {prestamo.id}, Miembro ID: {prestamo.miembro_id}")

if __name__ == "__main__":
    test_eliminar_miembro()
    verificar_integridad() 