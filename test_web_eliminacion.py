#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script que simula exactamente la eliminación web
"""

from main import app, db
from models import Miembro, PrestamoInterno
from flask import request

def test_eliminacion_web():
    """Simula exactamente la eliminación web"""
    
    with app.app_context():
        print("=== SIMULANDO ELIMINACIÓN WEB ===")
        
        # Obtener el miembro
        miembro = Miembro.query.first()
        if not miembro:
            print("No hay miembros para eliminar")
            return
        
        print(f"Miembro: {miembro.nombre_completo} (ID: {miembro.id})")
        
        # Simular la función exacta de la web
        try:
            # Verificar préstamos antes de eliminar
            prestamos_activos = PrestamoInterno.query.filter_by(miembro_id=miembro.id, estado='activo').count()
            prestamos_todos = PrestamoInterno.query.filter_by(miembro_id=miembro.id).count()
            print(f"Préstamos activos: {prestamos_activos}")
            print(f"Total préstamos: {prestamos_todos}")
            
            if prestamos_activos > 0:
                print("❌ NO SE PUEDE ELIMINAR - TIENE PRÉSTAMOS ACTIVOS")
                return

            # Eliminar todos los préstamos del miembro
            print("1. Eliminando préstamos del miembro...")
            prestamos_miembro = PrestamoInterno.query.filter_by(miembro_id=miembro.id).all()
            for prestamo in prestamos_miembro:
                print(f"   Eliminando préstamo ID: {prestamo.id}, Estado: {prestamo.estado}")
                db.session.delete(prestamo)
            db.session.commit()
            print("   ✅ Préstamos eliminados")

            # Eliminar foto si existe
            if miembro.foto:
                import os
                foto_path = os.path.join(app.static_folder, miembro.foto)
                if os.path.exists(foto_path):
                    os.remove(foto_path)
                    print(f"   ✅ Foto eliminada: {foto_path}")

            # Ahora eliminar el miembro
            print("2. Eliminando miembro...")
            db.session.delete(miembro)
            db.session.commit()
            print("   ✅ Miembro eliminado")
            
            print("✅ ELIMINACIÓN COMPLETADA CON ÉXITO")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ ERROR AL ELIMINAR MIEMBRO:")
            print(f"   Tipo de error: {type(e).__name__}")
            print(f"   Mensaje: {str(e)}")
            print(f"   Error completo: {e}")

if __name__ == "__main__":
    test_eliminacion_web() 