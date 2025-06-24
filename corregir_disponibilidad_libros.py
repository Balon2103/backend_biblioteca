from main import app, db
from models import Libro, Prestamo, PersonaPrestamo

def corregir_disponibilidad_libros():
    """Corrige la disponibilidad de los libros basándose en los préstamos reales"""
    with app.app_context():
        try:
            print("🔄 Corrigiendo disponibilidad de libros...")
            
            # Primero, marcar todos los libros como disponibles
            Libro.query.update({Libro.disponible: True})
            db.session.commit()
            print("✅ Todos los libros marcados como disponibles inicialmente")
            
            # Obtener todos los préstamos activos (internos y externos)
            prestamos_activos = Prestamo.query.filter_by(estado='activo').all()
            prestamos_externos_activos = PersonaPrestamo.query.filter_by(estado='activo').all()
            
            print(f"📊 Préstamos internos activos: {len(prestamos_activos)}")
            print(f"📊 Préstamos externos activos: {len(prestamos_externos_activos)}")
            
            # Marcar como no disponibles los libros que están prestados
            libros_prestados = set()
            
            for prestamo in prestamos_activos:
                libros_prestados.add(prestamo.libro_id)
                print(f"  - Libro ID {prestamo.libro_id} prestado (interno)")
            
            for prestamo in prestamos_externos_activos:
                libros_prestados.add(prestamo.libro_id)
                print(f"  - Libro ID {prestamo.libro_id} prestado (externo)")
            
            # Actualizar disponibilidad
            for libro_id in libros_prestados:
                libro = Libro.query.get(libro_id)
                if libro:
                    libro.disponible = False
                    print(f"  - Libro '{libro.titulo}' marcado como NO disponible")
            
            db.session.commit()
            
            # Mostrar estadísticas finales
            total_libros = Libro.query.count()
            libros_disponibles = Libro.query.filter_by(disponible=True).count()
            libros_prestados_count = Libro.query.filter_by(disponible=False).count()
            
            print("\n📊 Estadísticas finales:")
            print(f"  - Total de libros: {total_libros}")
            print(f"  - Libros disponibles: {libros_disponibles}")
            print(f"  - Libros prestados: {libros_prestados_count}")
            print(f"  - Préstamos activos totales: {len(prestamos_activos) + len(prestamos_externos_activos)}")
            
            if len(prestamos_activos) + len(prestamos_externos_activos) != libros_prestados_count:
                print("⚠️  ADVERTENCIA: El número de libros prestados no coincide con los préstamos activos")
                print("   Esto puede indicar préstamos duplicados o inconsistencias en la base de datos")
            
            print("✅ Disponibilidad de libros corregida exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al corregir disponibilidad: {str(e)}")

if __name__ == '__main__':
    corregir_disponibilidad_libros() 