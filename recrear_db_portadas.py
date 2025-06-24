#!/usr/bin/env python3
"""
Script para recrear la base de datos con la nueva estructura incluyendo portadas
"""

import os
from main import app, db
from models import Usuario, Libro, Miembro, PrestamoInterno, PersonaPrestamo

def recrear_base_datos():
    with app.app_context():
        try:
            # Eliminar la base de datos existente
            if os.path.exists('biblioteca.db'):
                os.remove('biblioteca.db')
                print("Base de datos anterior eliminada")
            
            # Crear todas las tablas
            db.create_all()
            print("Nueva base de datos creada con todas las tablas")
            
            # Crear usuarios administradores
            superadmin = Usuario(
                username='superadmin',
                nombre='Super',
                apellido='Administrador',
                cedula='0000000000',
                email='superadmin@biblioteca.com',
                telefono='0000000000',
                rol='superadmin'
            )
            superadmin.set_password('superadmin123')
            
            admin = Usuario(
                username='admin',
                nombre='Admin',
                apellido='Sistema',
                cedula='0000000001',
                email='admin@biblioteca.com',
                telefono='0000000001',
                rol='admin'
            )
            admin.set_password('admin123')
            
            db.session.add(superadmin)
            db.session.add(admin)
            db.session.commit()
            print("Usuarios administradores creados")
            
            print("Base de datos recreada exitosamente")
            
        except Exception as e:
            print(f"Error al recrear la base de datos: {str(e)}")

if __name__ == '__main__':
    recrear_base_datos() 