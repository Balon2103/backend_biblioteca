#!/usr/bin/env python3
"""
Script para recrear la base de datos con los nuevos campos
"""

import os
from main import app, db
from models import Libro, Usuario, Prestamo, PersonaPrestamo, Miembro
import json

def recrear_base_datos():
    with app.app_context():
        try:
            # Hacer backup de datos existentes
            print("Haciendo backup de datos existentes...")
            
            # Backup de libros
            libros_data = []
            if os.path.exists('biblioteca.db'):
                libros = Libro.query.all()
                for libro in libros:
                    libros_data.append({
                        'titulo': libro.titulo,
                        'autor': libro.autor,
                        'cota': libro.cota,
                        'verificacion': libro.verificacion,
                        'anio_edicion': libro.anio_edicion,
                        'medidas': libro.medidas,
                        'num_paginas': libro.num_paginas,
                        'ciudad': libro.ciudad,
                        'editorial': libro.editorial,
                        'coleccion': libro.coleccion,
                        'materias': libro.materias,
                        'caract_formato': libro.caract_formato,
                        'cant_ejemplares': libro.cant_ejemplares,
                        'tomos': libro.tomos,
                        'disponible': libro.disponible
                    })
            
            # Eliminar base de datos existente
            if os.path.exists('biblioteca.db'):
                os.remove('biblioteca.db')
                print("Base de datos anterior eliminada")
            
            # Crear nueva base de datos
            print("Creando nueva base de datos...")
            db.create_all()
            
            # Restaurar libros
            if libros_data:
                print(f"Restaurando {len(libros_data)} libros...")
                for libro_data in libros_data:
                    libro = Libro(**libro_data)
                    db.session.add(libro)
                db.session.commit()
                print("Libros restaurados exitosamente")
            
            # Crear usuarios administradores
            print("Creando usuarios administradores...")
            
            superadmin = Usuario(
                username='superadmin',
                nombre='Super',
                apellido='Administrador',
                cedula='0000000000',
                email='superadmin@biblioteca.com',
                telefono='0000000000',
                rol='superadmin',
                is_admin=True
            )
            superadmin.set_password('superadmin123')
            db.session.add(superadmin)
            
            admin = Usuario(
                username='admin',
                nombre='Admin',
                apellido='Sistema',
                cedula='0000000001',
                email='admin@biblioteca.com',
                telefono='0000000001',
                rol='admin',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            db.session.commit()
            print("Usuarios administradores creados")
            
            print("Base de datos recreada exitosamente")
            
        except Exception as e:
            print(f"Error al recrear la base de datos: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    recrear_base_datos() 