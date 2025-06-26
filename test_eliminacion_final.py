#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba final para la eliminación de miembros
"""

from main import app, db
from models import Miembro, PrestamoInterno

def test_eliminacion_final():
    """Prueba la eliminación usando la función real"""
    
    with app.app_context():
        print("=== PRUEBA FINAL DE ELIMINACIÓN ===")
        
        # Obtener el miembro
        miembro = Miembro.query.first()
        if not miembro:
            print("No se encontró ningún miembro")
            return
        
        print(f"Miembro a eliminar:")
        print(f"  ID: {miembro.id}")
        print(f"  Nombre: {miembro.nombre_completo}")
        print(f"  Cédula: {miembro.cedula}")
        
        # Verificar préstamos
        prestamos_activos = PrestamoInterno.query.filter_by(miembro_id=miembro.id, estado='activo').count()
        prestamos_todos = PrestamoInterno.query.filter_by(miembro_id=miembro.id).count()
        
        print(f"  Préstamos activos: {prestamos_activos}")
        print(f"  Total préstamos: {prestamos_todos}")
        
        if prestamos_activos > 0:
            print("⚠️  El miembro tiene préstamos activos. No se puede eliminar.")
            return
        
        # Simular la función de eliminación
        try:
            print("\n1. Eliminando préstamos del miembro...")
            prestamos_miembro = PrestamoInterno.query.filter_by(miembro_id=miembro.id).all()
            for prestamo in prestamos_miembro:
                print(f"   Eliminando préstamo ID: {prestamo.id}")
                db.session.delete(prestamo)
            db.session.commit()
            print("   ✅ Préstamos eliminados")
            
            print("\n2. Eliminando miembro...")
            db.session.delete(miembro)
            db.session.commit()
            print("   ✅ Miembro eliminado")
            
            print("\n✅ ELIMINACIÓN EXITOSA")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {str(e)}")
            print(f"Tipo de error: {type(e).__name__}")

if __name__ == "__main__":
    test_eliminacion_final() 