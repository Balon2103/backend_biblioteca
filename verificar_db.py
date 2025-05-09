from app import app
from models import Libro
from extensions import db

with app.app_context():
    total_libros = Libro.query.count()
    print(f"\nTotal de libros en la base de datos: {total_libros}")
    
    if total_libros > 0:
        print("\nPrimeros 5 libros:")
        libros = Libro.query.limit(5).all()
        for libro in libros:
            print(f"\nID: {libro.id}")
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Editorial: {libro.editorial}")
            print("-" * 50)
    else:
        print("\nNo hay libros en la base de datos.") 