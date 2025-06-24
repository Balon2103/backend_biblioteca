from main import db, app
from models import Libro
from app.utils.google_books import buscar_portada_libro
import time

def actualizar_portadas():
    with app.app_context():
        # Obtener todos los libros
        libros = Libro.query.all()
        total_libros = len(libros)
        actualizados = 0
        
        print(f"Total de libros a procesar: {total_libros}")
        
        for libro in libros:
            print(f"\nBuscando portada para: {libro.titulo} ({libro.autor})")
            
            # Si ya tiene portada, saltar
            if libro.portada_url:
                print(f"Ya tiene portada: {libro.portada_url}")
                continue
            
            # Buscar portada con todos los datos disponibles
            portada_url = buscar_portada_libro(
                titulo=libro.titulo,
                autor=libro.autor,
                editorial=libro.editorial,
                anio=str(libro.anio_edicion) if libro.anio_edicion else None
            )
            
            if portada_url:
                libro.portada_url = portada_url
                try:
                    db.session.commit()
                    print(f"Portada encontrada y actualizada para: {libro.titulo}")
                    actualizados += 1
                except Exception as e:
                    db.session.rollback()
                    print(f"Error al guardar la portada: {str(e)}")
            else:
                print(f"No se encontró portada para: {libro.titulo}")
            
            # Esperar un poco para no sobrecargar la API
            time.sleep(1)
        
        print(f"\nProceso completado. Portadas actualizadas: {actualizados} de {total_libros}")

if __name__ == "__main__":
    actualizar_portadas() 