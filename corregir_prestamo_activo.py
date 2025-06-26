#!/usr/bin/env python3
"""
Script para encontrar y corregir préstamos que están marcados como activos 
cuando deberían estar como devueltos
"""

from main import app, db
from models import Libro, Prestamo, PrestamoInterno, PersonaPrestamo, Miembro, Usuario
from datetime import datetime

def corregir_prestamo_activo():
    with app.app_context():
        print("=== CORRECCIÓN DE PRÉSTAMO ACTIVO ===")
        
        # Buscar préstamos activos en todos los modelos
        prestamos_activos = Prestamo.query.filter_by(estado='activo').all()
        prestamos_internos_activos = PrestamoInterno.query.filter_by(estado='activo').all()
        prestamos_externos_activos = PersonaPrestamo.query.filter_by(estado='activo').all()
        
        print(f"📋 PRÉSTAMOS ACTIVOS ENCONTRADOS:")
        print(f"   - Prestamo (antiguo): {len(prestamos_activos)}")
        print(f"   - PrestamoInterno: {len(prestamos_internos_activos)}")
        print(f"   - PersonaPrestamo: {len(prestamos_externos_activos)}")
        
        # Mostrar detalles de cada préstamo activo
        for i, prestamo in enumerate(prestamos_activos, 1):
            libro = Libro.query.get(prestamo.libro_id)
            usuario = Usuario.query.get(prestamo.usuario_id)
            print(f"\n{i}. PRÉSTAMO (antiguo) - ID: {prestamo.id}")
            print(f"   Libro: {libro.titulo if libro else 'No encontrado'}")
            print(f"   Usuario: {usuario.nombre if usuario else 'No encontrado'}")
            print(f"   Fecha préstamo: {prestamo.fecha_prestamo}")
            print(f"   Fecha devolución esperada: {prestamo.fecha_devolucion_esperada}")
            print(f"   Estado: {prestamo.estado}")
            print(f"   Libro disponible: {libro.disponible if libro else 'N/A'}")
        
        for i, prestamo in enumerate(prestamos_internos_activos, 1):
            libro = Libro.query.get(prestamo.libro_id)
            miembro = Miembro.query.get(prestamo.miembro_id)
            print(f"\n{i}. PRÉSTAMO INTERNO - ID: {prestamo.id}")
            print(f"   Libro: {libro.titulo if libro else 'No encontrado'}")
            print(f"   Miembro: {miembro.nombre_completo if miembro else 'No encontrado'}")
            print(f"   Fecha préstamo: {prestamo.fecha_prestamo}")
            print(f"   Fecha devolución esperada: {prestamo.fecha_devolucion_esperada}")
            print(f"   Estado: {prestamo.estado}")
            print(f"   Libro disponible: {libro.disponible if libro else 'N/A'}")
        
        for i, prestamo in enumerate(prestamos_externos_activos, 1):
            libro = Libro.query.get(prestamo.libro_id)
            print(f"\n{i}. PRÉSTAMO EXTERNO - ID: {prestamo.id}")
            print(f"   Libro: {libro.titulo if libro else 'No encontrado'}")
            print(f"   Nombre: {prestamo.nombre}")
            print(f"   Fecha préstamo: {prestamo.fecha_prestamo}")
            print(f"   Fecha devolución esperada: {prestamo.fecha_devolucion_esperada}")
            print(f"   Estado: {prestamo.estado}")
            print(f"   Libro disponible: {libro.disponible if libro else 'N/A'}")
        
        # Buscar préstamos devueltos para comparar
        prestamos_devueltos = Prestamo.query.filter_by(estado='devuelto').all()
        prestamos_internos_devueltos = PrestamoInterno.query.filter_by(estado='devuelto').all()
        prestamos_externos_devueltos = PersonaPrestamo.query.filter_by(estado='devuelto').all()
        
        print(f"\n📋 PRÉSTAMOS DEVUELTOS ENCONTRADOS:")
        print(f"   - Prestamo (antiguo): {len(prestamos_devueltos)}")
        print(f"   - PrestamoInterno: {len(prestamos_internos_devueltos)}")
        print(f"   - PersonaPrestamo: {len(prestamos_externos_devueltos)}")
        
        # Mostrar detalles de préstamos devueltos
        for i, prestamo in enumerate(prestamos_devueltos, 1):
            libro = Libro.query.get(prestamo.libro_id)
            usuario = Usuario.query.get(prestamo.usuario_id)
            print(f"\n{i}. PRÉSTAMO DEVUELTO (antiguo) - ID: {prestamo.id}")
            print(f"   Libro: {libro.titulo if libro else 'No encontrado'}")
            print(f"   Usuario: {usuario.nombre if usuario else 'No encontrado'}")
            print(f"   Fecha préstamo: {prestamo.fecha_prestamo}")
            print(f"   Fecha devolución: {prestamo.fecha_devolucion_real}")
            print(f"   Estado: {prestamo.estado}")
            print(f"   Libro disponible: {libro.disponible if libro else 'N/A'}")
        
        for i, prestamo in enumerate(prestamos_internos_devueltos, 1):
            libro = Libro.query.get(prestamo.libro_id)
            miembro = Miembro.query.get(prestamo.miembro_id)
            print(f"\n{i}. PRÉSTAMO INTERNO DEVUELTO - ID: {prestamo.id}")
            print(f"   Libro: {libro.titulo if libro else 'No encontrado'}")
            print(f"   Miembro: {miembro.nombre_completo if miembro else 'No encontrado'}")
            print(f"   Fecha préstamo: {prestamo.fecha_prestamo}")
            print(f"   Fecha devolución: {prestamo.fecha_devolucion_real}")
            print(f"   Estado: {prestamo.estado}")
            print(f"   Libro disponible: {libro.disponible if libro else 'N/A'}")
        
        # Preguntar si quiere corregir algún préstamo
        if prestamos_activos or prestamos_internos_activos or prestamos_externos_activos:
            print(f"\n🔧 ¿Deseas marcar algún préstamo como devuelto? (s/n): ", end="")
            respuesta = input().lower()
            
            if respuesta == 's':
                print("Ingresa el tipo de préstamo (1=Prestamo, 2=PrestamoInterno, 3=PersonaPrestamo): ", end="")
                tipo = input().strip()
                
                print("Ingresa el ID del préstamo: ", end="")
                prestamo_id = int(input().strip())
                
                try:
                    if tipo == '1':
                        prestamo = Prestamo.query.get(prestamo_id)
                        if prestamo and prestamo.estado == 'activo':
                            prestamo.estado = 'devuelto'
                            prestamo.fecha_devolucion_real = datetime.utcnow()
                            libro = Libro.query.get(prestamo.libro_id)
                            if libro:
                                libro.disponible = True
                            print(f"✅ Préstamo {prestamo_id} marcado como devuelto")
                        else:
                            print("❌ Préstamo no encontrado o ya no está activo")
                    elif tipo == '2':
                        prestamo = PrestamoInterno.query.get(prestamo_id)
                        if prestamo and prestamo.estado == 'activo':
                            prestamo.estado = 'devuelto'
                            prestamo.fecha_devolucion_real = datetime.utcnow()
                            libro = Libro.query.get(prestamo.libro_id)
                            if libro:
                                libro.disponible = True
                            print(f"✅ Préstamo interno {prestamo_id} marcado como devuelto")
                        else:
                            print("❌ Préstamo interno no encontrado o ya no está activo")
                    elif tipo == '3':
                        prestamo = PersonaPrestamo.query.get(prestamo_id)
                        if prestamo and prestamo.estado == 'activo':
                            prestamo.estado = 'devuelto'
                            prestamo.fecha_devolucion_real = datetime.utcnow()
                            libro = Libro.query.get(prestamo.libro_id)
                            if libro:
                                libro.disponible = True
                            print(f"✅ Préstamo externo {prestamo_id} marcado como devuelto")
                        else:
                            print("❌ Préstamo externo no encontrado o ya no está activo")
                    else:
                        print("❌ Tipo de préstamo inválido")
                        return
                    
                    db.session.commit()
                    print("✅ Cambios guardados en la base de datos")
                    
                except Exception as e:
                    print(f"❌ Error al corregir el préstamo: {str(e)}")
                    db.session.rollback()
            else:
                print("ℹ️ No se realizaron correcciones")
        else:
            print("✅ No hay préstamos activos para corregir")
        
        print(f"\n=== FIN DE CORRECCIÓN ===")

if __name__ == "__main__":
    corregir_prestamo_activo() 