#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para devolver préstamos activos de un miembro
"""

from main import app, db
from models import Miembro, PrestamoInterno, Libro
from datetime import datetime

def devolver_prestamos_activos():
    """Devuelve todos los préstamos activos de un miembro"""
    
    with app.app_context():
        print("=== DEVOLUCIÓN DE PRÉSTAMOS ACTIVOS ===")
        
        # Obtener el miembro
        miembro = Miembro.query.first()
        if not miembro:
            print("No se encontró ningún miembro")
            return
        
        print(f"Miembro: {miembro.nombre_completo} (ID: {miembro.id})")
        
        # Buscar préstamos activos
        prestamos_activos = PrestamoInterno.query.filter_by(
            miembro_id=miembro.id, 
            estado='activo'
        ).all()
        
        print(f"Préstamos activos encontrados: {len(prestamos_activos)}")
        
        if len(prestamos_activos) == 0:
            print("No hay préstamos activos para devolver")
            return
        
        # Devolver cada préstamo activo
        for prestamo in prestamos_activos:
            try:
                print(f"\nDevolviendo préstamo ID: {prestamo.id}")
                print(f"  Libro: {prestamo.libro.titulo if prestamo.libro else 'Libro no encontrado'}")
                print(f"  Fecha préstamo: {prestamo.fecha_prestamo}")
                print(f"  Fecha devolución esperada: {prestamo.fecha_devolucion_esperada}")
                
                # Marcar como devuelto
                prestamo.estado = 'devuelto'
                prestamo.fecha_devolucion_real = datetime.utcnow()
                
                # Marcar libro como disponible
                if prestamo.libro:
                    prestamo.libro.disponible = True
                    print(f"  Libro marcado como disponible: {prestamo.libro.titulo}")
                
                print(f"  ✅ Préstamo devuelto exitosamente")
                
            except Exception as e:
                print(f"  ❌ Error al devolver préstamo: {str(e)}")
                db.session.rollback()
                return
        
        # Confirmar cambios
        try:
            db.session.commit()
            print(f"\n✅ Todos los préstamos activos han sido devueltos")
            
            # Verificar estado final
            prestamos_activos_final = PrestamoInterno.query.filter_by(
                miembro_id=miembro.id, 
                estado='activo'
            ).count()
            
            print(f"Préstamos activos restantes: {prestamos_activos_final}")
            
            if prestamos_activos_final == 0:
                print("✅ El miembro ya no tiene préstamos activos y puede ser eliminado")
            else:
                print("⚠️  Aún quedan préstamos activos")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al confirmar cambios: {str(e)}")

def eliminar_miembro_sin_prestamos():
    """Elimina un miembro que no tiene préstamos activos"""
    
    with app.app_context():
        print("\n=== ELIMINACIÓN DE MIEMBRO ===")
        
        # Obtener el miembro
        miembro = Miembro.query.first()
        if not miembro:
            print("No se encontró ningún miembro")
            return
        
        # Verificar que no tenga préstamos activos
        prestamos_activos = PrestamoInterno.query.filter_by(
            miembro_id=miembro.id, 
            estado='activo'
        ).count()
        
        if prestamos_activos > 0:
            print(f"⚠️  El miembro aún tiene {prestamos_activos} préstamo(s) activo(s)")
            print("Primero debe devolver todos los préstamos activos")
            return
        
        print(f"Eliminando miembro: {miembro.nombre_completo} (ID: {miembro.id})")
        
        try:
            # Eliminar foto si existe
            if miembro.foto:
                import os
                foto_path = os.path.join(app.static_folder, miembro.foto)
                if os.path.exists(foto_path):
                    os.remove(foto_path)
                    print(f"Foto eliminada: {foto_path}")
            
            # Eliminar de la base de datos
            db.session.delete(miembro)
            db.session.commit()
            
            print("✅ Miembro eliminado exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al eliminar miembro: {str(e)}")

if __name__ == "__main__":
    devolver_prestamos_activos()
    eliminar_miembro_sin_prestamos() 