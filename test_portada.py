from app.utils.google_books import buscar_portada_libro

# Prueba con un libro conocido
isbn = "9788497592208"  # ISBN de "Cien años de soledad"
titulo = "Cien años de soledad"
autor = "Gabriel García Márquez"

# Intentar buscar la portada
portada_url = buscar_portada_libro(isbn=isbn, titulo=titulo, autor=autor)
print(f"URL de la portada: {portada_url}") 