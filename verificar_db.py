#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar la estructura actual de la base de datos
"""

import sqlite3

DB_PATH = "biblioteca.db"

def verificar_estructura_db():
    """Verifica la estructura actual de la base de datos"""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("=== VERIFICACIÓN DE ESTRUCTURA DE BASE DE DATOS ===")
    
    # Verificar tabla prestamos_internos
    print("\n1. Estructura de tabla prestamos_internos:")
    c.execute("PRAGMA table_info(prestamos_internos);")
    columns = c.fetchall()
    for col in columns:
        print(f"   {col[1]} {col[2]} {'NULL' if col[3] else 'NOT NULL'}")
    
    # Verificar claves foráneas
    print("\n2. Claves foráneas de prestamos_internos:")
    c.execute("PRAGMA foreign_key_list('prestamos_internos');")
    foreign_keys = c.fetchall()
    for fk in foreign_keys:
        print(f"   {fk[3]} -> {fk[4]}.{fk[5]} (ON DELETE: {fk[6]})")
    
    # Verificar datos actuales
    print("\n3. Datos actuales:")
    c.execute("SELECT COUNT(*) FROM prestamos_internos;")
    count = c.fetchone()[0]
    print(f"   Total préstamos internos: {count}")
    
    if count > 0:
        c.execute("SELECT id, miembro_id, libro_id, estado FROM prestamos_internos LIMIT 5;")
        prestamos = c.fetchall()
        for prestamo in prestamos:
            print(f"   Préstamo ID: {prestamo[0]}, Miembro ID: {prestamo[1]}, Libro ID: {prestamo[2]}, Estado: {prestamo[3]}")
    
    c.execute("SELECT COUNT(*) FROM miembros;")
    count = c.fetchone()[0]
    print(f"   Total miembros: {count}")
    
    conn.close()

if __name__ == "__main__":
    verificar_estructura_db() 