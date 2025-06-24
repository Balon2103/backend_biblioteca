from main import app, db
from models import Libro

with app.app_context():
    # Obtener todos los libros
    libros = Libro.query.all()

    print("Libros en la base de datos:")
    for libro in libros:
        print(f"\nTítulo: {getattr(libro, 'titulo', 'N/A')}")
        print(f"ISBN: {getattr(libro, 'isbn', 'N/A')}")
        print(f"Portada URL: {getattr(libro, 'portada_url', 'N/A')}") 