from main import app, db
from models import Libro
from app.utils.google_books import buscar_portada_libro
from sqlalchemy import or_

# Diccionario de libros con sus ISBNs conocidos
libros_isbn = {
    "Cien años de soledad": "9788497592208",
    "El código Da Vinci": "9788497592208",
    "Don Quijote de la mancha": "9788420412146",
    "El principito": "9788498381492",
    "El señor de los anillos": "9788445000667",
    "Harry Potter y la piedra filosofal": "9788478884452",
    "1984": "9788497594752",
    "Los miserables": "9788491051884",
    "El retrato de Dorian Gray": "9788491051884",
    "Orgullo y prejuicio": "9788491051884",
    "El alquimista": "9788497592208",
    "El nombre del viento": "9788497592208",
    "Los juegos del hambre": "9788497592208",
    "El hobbit": "9788445000667",
    "Crimen y castigo": "9788491051884",
    "El perfume": "9788497592208",
    "El guardián entre el centeno": "9788497592208",
    "Las aventuras de Alicia en el país de las maravillas": "9788491051884",
    "El gran Gatsby": "9788497592208",
    "El conde de Montecristo": "9788491051884"
}

def actualizar_libros():
    with app.app_context():
        for titulo, isbn in libros_isbn.items():
            # Buscar el libro por título (búsqueda más flexible)
            libro = Libro.query.filter(
                or_(
                    Libro.titulo.ilike(f"%{titulo}%"),
                    Libro.titulo.ilike(f"{titulo}%"),
                    Libro.titulo.ilike(f"%{titulo}")
                )
            ).first()
            
            if libro:
                print(f"Actualizando {libro.titulo}...")
                libro.isbn = isbn
                # Buscar y actualizar la portada
                portada_url = buscar_portada_libro(isbn=isbn, titulo=titulo)
                if portada_url:
                    libro.portada_url = portada_url
                    print(f"Portada encontrada para {libro.titulo}")
                else:
                    print(f"No se encontró portada para {libro.titulo}")
            else:
                print(f"No se encontró el libro: {titulo}")
        
        try:
            # Guardar los cambios
            db.session.commit()
            print("\nActualización completada!")
        except Exception as e:
            print(f"\nError al guardar los cambios: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    actualizar_libros() 