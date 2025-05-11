import sqlite3
import os
from datetime import datetime

def actualizar_base_datos():
    # Crear backup de la base de datos actual
    if os.path.exists('biblioteca.db'):
        backup_name = f'biblioteca_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename('biblioteca.db', backup_name)
        print(f"Backup creado: {backup_name}")
    
    # Conectar a la base de datos
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    
    # Crear la tabla usuarios con el nuevo campo rol
    cursor.execute('''
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(80) UNIQUE NOT NULL,
        password_hash VARCHAR(128),
        is_admin BOOLEAN DEFAULT FALSE,
        rol VARCHAR(20) DEFAULT 'usuario',
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        cedula VARCHAR(20) UNIQUE,
        email VARCHAR(120) UNIQUE,
        telefono VARCHAR(20)
    )
    ''')
    
    # Crear el usuario superadmin
    cursor.execute('''
    INSERT INTO usuarios (username, password_hash, is_admin, rol, nombre, apellido, cedula, email, telefono)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'superadmin',
        'pbkdf2:sha256:600000$your_hash_here',  # Esto se actualizará al iniciar la aplicación
        True,
        'superadmin',
        'Super',
        'Admin',
        '0000000000',
        'superadmin@biblioteca.com',
        '0000000000'
    ))
    
    # Crear el usuario admin
    cursor.execute('''
    INSERT INTO usuarios (username, password_hash, is_admin, rol, nombre, apellido, cedula, email, telefono)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'admin',
        'pbkdf2:sha256:600000$your_hash_here',  # Esto se actualizará al iniciar la aplicación
        True,
        'admin',
        'Admin',
        'Sistema',
        '0000000001',
        'admin@biblioteca.com',
        '0000000001'
    ))
    
    # Crear las otras tablas necesarias
    cursor.execute('''
    CREATE TABLE libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo VARCHAR(200),
        autor VARCHAR(200),
        cota VARCHAR(50),
        verificacion VARCHAR(50),
        anio_edicion VARCHAR(20),
        medidas VARCHAR(50),
        num_paginas VARCHAR(20),
        ciudad VARCHAR(100),
        editorial VARCHAR(200),
        coleccion VARCHAR(200),
        materias TEXT,
        caract_formato VARCHAR(100),
        cant_ejemplares VARCHAR(20),
        tomos VARCHAR(50),
        disponible BOOLEAN DEFAULT TRUE
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE prestamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        libro_id INTEGER NOT NULL,
        fecha_prestamo DATETIME NOT NULL,
        fecha_devolucion_esperada DATETIME NOT NULL,
        fecha_devolucion_real DATETIME,
        estado VARCHAR(20) DEFAULT 'activo',
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
        FOREIGN KEY (libro_id) REFERENCES libros (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE personas_prestamo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        cedula VARCHAR(50) NOT NULL,
        direccion VARCHAR(200) NOT NULL,
        telefono VARCHAR(50) NOT NULL,
        email VARCHAR(120) NOT NULL,
        observaciones TEXT,
        fecha_prestamo DATETIME NOT NULL,
        fecha_devolucion_esperada DATETIME NOT NULL,
        fecha_devolucion_real DATETIME,
        estado VARCHAR(20) DEFAULT 'activo',
        libro_id INTEGER NOT NULL,
        FOREIGN KEY (libro_id) REFERENCES libros (id)
    )
    ''')
    
    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    
    print("Base de datos actualizada exitosamente")
    print("\nUsuarios creados:")
    print("1. Superadmin")
    print("   Usuario: superadmin")
    print("   Contraseña: superadmin123")
    print("\n2. Admin")
    print("   Usuario: admin")
    print("   Contraseña: admin123")

if __name__ == '__main__':
    actualizar_base_datos() 