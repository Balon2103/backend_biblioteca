#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script simple para corregir préstamos activos
"""

from main import app, db
from models import PrestamoInterno, Libro
from datetime import datetime

def corregir_prestamo_activo():
    """Corrige el préstamo activo marcándolo como devuelto"""
    
    with app.app_context():
        print("=== CORRECCIÓN DE PRÉSTAMO ACTIVO ===")
        
        # Buscar el préstamo activo específico
        prestamo_activo = PrestamoInterno.query.filter_by(id=3, estado='activo').first()
        
        if not prestamo_activo:
            print("No se encontró el préstamo activo con ID 3")
            return
        
        print(f"Préstamo encontrado:")
        print(f"  ID: {prestamo_activo.id}")
        print(f"  Miembro ID: {prestamo_activo.miembro_id}")
        print(f"  Libro ID: {prestamo_activo.libro_id}")
        print(f"  Estado actual: {prestamo_activo.estado}")
        
        try:
            # Solo cambiar el estado y la fecha de devolución
            prestamo_activo.estado = 'devuelto'
            prestamo_activo.fecha_devolucion_real = datetime.utcnow()
            
            # También marcar el libro como disponible
            libro = Libro.query.get(prestamo_activo.libro_id)
            if libro:
                libro.disponible = True
                print(f"  Libro marcado como disponible: {libro.titulo}")
            
            db.session.commit()
            print("✅ Préstamo marcado como devuelto exitosamente")
            
            # Verificar el cambio
            prestamo_verificado = PrestamoInterno.query.get(3)
            print(f"  Estado después del cambio: {prestamo_verificado.estado}")
            print(f"  Fecha devolución real: {prestamo_verificado.fecha_devolucion_real}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}")

def verificar_estado_final():
    """Verifica el estado final de los préstamos"""
    
    with app.app_context():
        print("\n=== VERIFICACIÓN FINAL ===")
        
        # Verificar todos los préstamos del miembro
        prestamos = PrestamoInterno.query.filter_by(miembro_id=1).all()
        
        print(f"Total de préstamos del miembro: {len(prestamos)}")
        
        for prestamo in prestamos:
            print(f"  Préstamo ID: {prestamo.id}")
            print(f"    Estado: {prestamo.estado}")
            print(f"    Libro: {prestamo.libro.titulo if prestamo.libro else 'No encontrado'}")
            print(f"    Fecha devolución real: {prestamo.fecha_devolucion_real}")
        
        # Verificar préstamos activos
        prestamos_activos = PrestamoInterno.query.filter_by(miembro_id=1, estado='activo').count()
        print(f"\nPréstamos activos restantes: {prestamos_activos}")
        
        if prestamos_activos == 0:
            print("✅ El miembro ya no tiene préstamos activos")
        else:
            print("⚠️  Aún quedan préstamos activos")

if __name__ == "__main__":
    corregir_prestamo_activo()
    verificar_estado_final() 