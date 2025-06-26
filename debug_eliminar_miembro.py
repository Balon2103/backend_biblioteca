#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para debuggear el error de eliminación de miembros
"""

from main import app, db
from models import Miembro, PrestamoInterno

def debug_eliminar_miembro():
    """Debuggea el proceso de eliminación de un miembro"""
    
    with app.app_context():
        print("=== DEBUG ELIMINACIÓN DE MIEMBRO ===")
        
        # Obtener el primer miembro
        miembro = Miembro.query.first()
        if not miembro:
            print("No se encontró ningún miembro")
            return
        
        print(f"Miembro a eliminar:")
        print(f"  ID: {miembro.id}")
        print(f"  Nombre: {miembro.nombre_completo}")
        print(f"  Cédula: {miembro.cedula}")
        
        # Verificar préstamos activos
        prestamos_activos = PrestamoInterno.query.filter_by(miembro_id=miembro.id, estado='activo').count()
        print(f"  Préstamos activos: {prestamos_activos}")
        
        # Verificar todos los préstamos
        prestamos_todos = PrestamoInterno.query.filter_by(miembro_id=miembro.id).count()
        print(f"  Total préstamos: {prestamos_todos}")
        
        if prestamos_activos > 0:
            print("⚠️  El miembro tiene préstamos activos. No se puede eliminar.")
            return
        
        # Intentar eliminar paso a paso
        try:
            print("\n1. Verificando foto...")
            if miembro.foto:
                import os
                foto_path = os.path.join(app.static_folder, miembro.foto)
                print(f"   Ruta de foto: {foto_path}")
                if os.path.exists(foto_path):
                    print(f"   Foto existe, intentando eliminar...")
                    os.remove(foto_path)
                    print(f"   ✅ Foto eliminada")
                else:
                    print(f"   ⚠️  Foto no existe en la ruta")
            else:
                print(f"   ✅ No tiene foto")
            
            print("\n2. Intentando eliminar de la base de datos...")
            
            # Verificar si hay restricciones de clave foránea
            print(f"   Verificando restricciones...")
            
            # Intentar eliminar
            db.session.delete(miembro)
            print(f"   ✅ Miembro marcado para eliminación")
            
            print(f"   Intentando commit...")
            db.session.commit()
            print(f"   ✅ Commit exitoso")
            
            print(f"\n✅ Miembro eliminado exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al eliminar miembro:")
            print(f"   Tipo de error: {type(e).__name__}")
            print(f"   Mensaje: {str(e)}")
            
            # Verificar si es un error de integridad referencial
            if "FOREIGN KEY constraint failed" in str(e) or "integrity" in str(e).lower():
                print(f"   🔍 Es un error de integridad referencial")
                print(f"   Esto significa que hay registros relacionados que impiden la eliminación")
                
                # Verificar qué registros están relacionados
                print(f"\n   Verificando registros relacionados...")
                
                # Verificar préstamos internos
                prestamos_relacionados = PrestamoInterno.query.filter_by(miembro_id=miembro.id).all()
                print(f"   Préstamos internos relacionados: {len(prestamos_relacionados)}")
                for prestamo in prestamos_relacionados:
                    print(f"     - Préstamo ID: {prestamo.id}, Estado: {prestamo.estado}")
            
            elif "no such table" in str(e).lower():
                print(f"   🔍 Error de tabla no encontrada")
            elif "permission" in str(e).lower():
                print(f"   🔍 Error de permisos")
            else:
                print(f"   🔍 Error desconocido")

if __name__ == "__main__":
    debug_eliminar_miembro() 