#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para recrear datos de prueba después de la migración
"""

from main import app, db
from models import Miembro, Libro, PrestamoInterno
from datetime import datetime, timedelta

def recrear_datos_prueba():
    """Recrea datos de prueba básicos"""
    
    with app.app_context():
        print("=== RECREANDO DATOS DE PRUEBA ===")
        
        # Verificar si ya existen datos
        if Miembro.query.count() > 0:
            print("Ya existen datos en la base de datos")
            return
        
        # Crear miembro de prueba
        print("Creando miembro de prueba...")
        miembro = Miembro(
            nombres="Juan",
            apellidos="Pérez",
            cedula="12345678",
            email="juan.perez@test.com",
            telefono="123456789",
            direccion="Dirección de prueba",
            numero_carnet="TEST001",
            estado="activo"
        )
        db.session.add(miembro)
        db.session.commit()
        print(f"✅ Miembro creado con ID: {miembro.id}")
        
        # Crear libro de prueba
        print("Creando libro de prueba...")
        libro = Libro(
            titulo="Libro de Prueba",
            autor="Autor de Prueba",
            editorial="Editorial de Prueba",
            disponible=True
        )
        db.session.add(libro)
        db.session.commit()
        print(f"✅ Libro creado con ID: {libro.id}")
        
        # Crear préstamo devuelto
        print("Creando préstamo devuelto...")
        prestamo = PrestamoInterno(
            miembro_id=miembro.id,
            libro_id=libro.id,
            fecha_prestamo=datetime.utcnow() - timedelta(days=30),
            fecha_devolucion_esperada=datetime.utcnow() - timedelta(days=15),
            fecha_devolucion_real=datetime.utcnow() - timedelta(days=15),
            estado='devuelto'
        )
        db.session.add(prestamo)
        db.session.commit()
        print(f"✅ Préstamo devuelto creado con ID: {prestamo.id}")
        
        print("\n=== DATOS DE PRUEBA CREADOS ===")
        print(f"Miembros: {Miembro.query.count()}")
        print(f"Libros: {Libro.query.count()}")
        print(f"Préstamos internos: {PrestamoInterno.query.count()}")

if __name__ == "__main__":
    recrear_datos_prueba() 