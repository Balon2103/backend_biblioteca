#!/usr/bin/env python3
"""
Script rápido para corregir el préstamo activo que debería estar devuelto
"""

from main import app, db
from models import Libro, Prestamo
from datetime import datetime

def corregir_rapido():
    with app.app_context():
        print("=== CORRECCIÓN RÁPIDA ===")
        
        # Buscar el préstamo activo
        prestamo_activo = Prestamo.query.filter_by(estado='activo').first()
        
        if prestamo_activo:
            print(f"Encontrado préstamo activo ID: {prestamo_activo.id}")
            print(f"Libro ID: {prestamo_activo.libro_id}")
            
            # Marcar como devuelto
            prestamo_activo.estado = 'devuelto'
            prestamo_activo.fecha_devolucion_real = datetime.utcnow()
            
            # Marcar libro como disponible
            libro = Libro.query.get(prestamo_activo.libro_id)
            if libro:
                libro.disponible = True
                print(f"Libro '{libro.titulo}' marcado como disponible")
            
            # Guardar cambios
            db.session.commit()
            print("✅ Préstamo marcado como devuelto correctamente")
        else:
            print("✅ No hay préstamos activos para corregir")
        
        print("=== FIN ===")

if __name__ == "__main__":
    corregir_rapido() 