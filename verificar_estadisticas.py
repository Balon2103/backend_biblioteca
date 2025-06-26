#!/usr/bin/env python3
"""
Script para verificar y corregir inconsistencias en las estadísticas de préstamos
"""

from main import app, db
from models import Libro, Prestamo, PrestamoInterno, PersonaPrestamo, Miembro
from datetime import datetime

def verificar_estadisticas():
    with app.app_context():
        print("=== VERIFICACIÓN DE ESTADÍSTICAS ===")
        
        # 1. Verificar libros
        total_libros = Libro.query.count()
        libros_disponibles = Libro.query.filter_by(disponible=True).count()
        libros_prestados = Libro.query.filter_by(disponible=False).count()
        
        print(f"📚 Total libros: {total_libros}")
        print(f"✅ Libros disponibles: {libros_disponibles}")
        print(f"📖 Libros prestados: {libros_prestados}")
        
        # 2. Verificar préstamos activos
        prestamos_activos = Prestamo.query.filter_by(estado='activo').count()
        prestamos_internos_activos = PrestamoInterno.query.filter_by(estado='activo').count()
        prestamos_externos_activos = PersonaPrestamo.query.filter_by(estado='activo').count()
        total_prestamos_activos = prestamos_activos + prestamos_internos_activos + prestamos_externos_activos
        
        print(f"\n📋 PRÉSTAMOS ACTIVOS:")
        print(f"   - Prestamo (antiguo): {prestamos_activos}")
        print(f"   - PrestamoInterno: {prestamos_internos_activos}")
        print(f"   - PersonaPrestamo: {prestamos_externos_activos}")
        print(f"   - TOTAL: {total_prestamos_activos}")
        
        # 3. Verificar préstamos devueltos
        prestamos_devueltos = Prestamo.query.filter_by(estado='devuelto').count()
        prestamos_internos_devueltos = PrestamoInterno.query.filter_by(estado='devuelto').count()
        prestamos_externos_devueltos = PersonaPrestamo.query.filter_by(estado='devuelto').count()
        total_prestamos_devueltos = prestamos_devueltos + prestamos_internos_devueltos + prestamos_externos_devueltos
        
        print(f"\n📋 PRÉSTAMOS DEVUELTOS:")
        print(f"   - Prestamo (antiguo): {prestamos_devueltos}")
        print(f"   - PrestamoInterno: {prestamos_internos_devueltos}")
        print(f"   - PersonaPrestamo: {prestamos_externos_devueltos}")
        print(f"   - TOTAL: {total_prestamos_devueltos}")
        
        # 4. Verificar inconsistencias
        print(f"\n🔍 VERIFICANDO INCONSISTENCIAS:")
        
        # Libros marcados como no disponibles sin préstamos activos
        libros_no_disponibles = Libro.query.filter_by(disponible=False).all()
        inconsistencias = []
        
        for libro in libros_no_disponibles:
            prestamo_activo = Prestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_interno_activo = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_externo_activo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            
            if not prestamo_activo and not prestamo_interno_activo and not prestamo_externo_activo:
                inconsistencias.append(f"Libro '{libro.titulo}' marcado como no disponible pero no tiene préstamos activos")
        
        # Libros marcados como disponibles con préstamos activos
        libros_disponibles = Libro.query.filter_by(disponible=True).all()
        
        for libro in libros_disponibles:
            prestamo_activo = Prestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_interno_activo = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_externo_activo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            
            if prestamo_activo or prestamo_interno_activo or prestamo_externo_activo:
                inconsistencias.append(f"Libro '{libro.titulo}' marcado como disponible pero tiene préstamos activos")
        
        if inconsistencias:
            print(f"❌ Se encontraron {len(inconsistencias)} inconsistencias:")
            for inconsistencia in inconsistencias:
                print(f"   - {inconsistencia}")
        else:
            print("✅ No se encontraron inconsistencias")
        
        # 5. Corregir inconsistencias si se solicita
        if inconsistencias:
            print(f"\n🔧 ¿Deseas corregir las inconsistencias? (s/n): ", end="")
            respuesta = input().lower()
            
            if respuesta == 's':
                cambios_realizados = []
                
                # Corregir libros no disponibles sin préstamos activos
                for libro in libros_no_disponibles:
                    prestamo_activo = Prestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
                    prestamo_interno_activo = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
                    prestamo_externo_activo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
                    
                    if not prestamo_activo and not prestamo_interno_activo and not prestamo_externo_activo:
                        libro.disponible = True
                        cambios_realizados.append(f"Libro '{libro.titulo}' marcado como disponible")
                
                # Corregir libros disponibles con préstamos activos
                for libro in libros_disponibles:
                    prestamo_activo = Prestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
                    prestamo_interno_activo = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
                    prestamo_externo_activo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
                    
                    if prestamo_activo or prestamo_interno_activo or prestamo_externo_activo:
                        libro.disponible = False
                        cambios_realizados.append(f"Libro '{libro.titulo}' marcado como no disponible")
                
                if cambios_realizados:
                    db.session.commit()
                    print(f"✅ Se realizaron {len(cambios_realizados)} correcciones:")
                    for cambio in cambios_realizados:
                        print(f"   - {cambio}")
                else:
                    print("ℹ️ No se realizaron correcciones")
            else:
                print("ℹ️ No se realizaron correcciones")
        
        print(f"\n=== FIN DE VERIFICACIÓN ===")

if __name__ == "__main__":
    verificar_estadisticas() 