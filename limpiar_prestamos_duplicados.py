from main import app, db
from models import Libro, Prestamo, PersonaPrestamo
from sqlalchemy import func

def limpiar_prestamos_duplicados():
    """Limpia préstamos duplicados y corrige la base de datos"""
    with app.app_context():
        try:
            print("🔄 Limpiando préstamos duplicados...")
            
            # Verificar préstamos internos duplicados
            print("\n📖 Verificando préstamos internos...")
            prestamos_internos = Prestamo.query.filter_by(estado='activo').all()
            libros_prestados_internos = {}
            
            for prestamo in prestamos_internos:
                libro_id = prestamo.libro_id
                if libro_id not in libros_prestados_internos:
                    libros_prestados_internos[libro_id] = [prestamo]
                else:
                    libros_prestados_internos[libro_id].append(prestamo)
            
            # Eliminar préstamos duplicados internos (mantener solo el más reciente)
            prestamos_a_eliminar = []
            for libro_id, prestamos in libros_prestados_internos.items():
                if len(prestamos) > 1:
                    print(f"  - Libro ID {libro_id}: {len(prestamos)} préstamos activos")
                    # Ordenar por fecha de préstamo (más reciente primero)
                    prestamos_ordenados = sorted(prestamos, key=lambda x: x.fecha_prestamo, reverse=True)
                    # Mantener solo el más reciente, eliminar los demás
                    for prestamo in prestamos_ordenados[1:]:
                        prestamos_a_eliminar.append(prestamo)
                        print(f"    - Eliminando préstamo ID {prestamo.id} (fecha: {prestamo.fecha_prestamo})")
            
            # Verificar préstamos externos duplicados
            print("\n📖 Verificando préstamos externos...")
            prestamos_externos = PersonaPrestamo.query.filter_by(estado='activo').all()
            libros_prestados_externos = {}
            
            for prestamo in prestamos_externos:
                libro_id = prestamo.libro_id
                if libro_id not in libros_prestados_externos:
                    libros_prestados_externos[libro_id] = [prestamo]
                else:
                    libros_prestados_externos[libro_id].append(prestamo)
            
            # Eliminar préstamos duplicados externos
            for libro_id, prestamos in libros_prestados_externos.items():
                if len(prestamos) > 1:
                    print(f"  - Libro ID {libro_id}: {len(prestamos)} préstamos externos activos")
                    # Ordenar por fecha de préstamo (más reciente primero)
                    prestamos_ordenados = sorted(prestamos, key=lambda x: x.fecha_prestamo, reverse=True)
                    # Mantener solo el más reciente, eliminar los demás
                    for prestamo in prestamos_ordenados[1:]:
                        prestamos_a_eliminar.append(prestamo)
                        print(f"    - Eliminando préstamo externo ID {prestamo.id} (fecha: {prestamo.fecha_prestamo})")
            
            # Eliminar los préstamos duplicados
            if prestamos_a_eliminar:
                print(f"\n🗑️  Eliminando {len(prestamos_a_eliminar)} préstamos duplicados...")
                for prestamo in prestamos_a_eliminar:
                    db.session.delete(prestamo)
                db.session.commit()
                print("✅ Préstamos duplicados eliminados")
            else:
                print("✅ No se encontraron préstamos duplicados")
            
            # Corregir disponibilidad de libros
            print("\n🔄 Corrigiendo disponibilidad de libros...")
            Libro.query.update({Libro.disponible: True})
            db.session.commit()
            
            # Obtener préstamos activos únicos
            prestamos_activos_unicos = Prestamo.query.filter_by(estado='activo').all()
            prestamos_externos_unicos = PersonaPrestamo.query.filter_by(estado='activo').all()
            
            libros_prestados = set()
            for prestamo in prestamos_activos_unicos:
                libros_prestados.add(prestamo.libro_id)
            for prestamo in prestamos_externos_unicos:
                libros_prestados.add(prestamo.libro_id)
            
            # Marcar libros como no disponibles
            for libro_id in libros_prestados:
                libro = Libro.query.get(libro_id)
                if libro:
                    libro.disponible = False
            
            db.session.commit()
            
            # Estadísticas finales
            total_libros = Libro.query.count()
            libros_disponibles = Libro.query.filter_by(disponible=True).count()
            libros_prestados_count = Libro.query.filter_by(disponible=False).count()
            
            print("\n📊 Estadísticas finales:")
            print(f"  - Total de libros: {total_libros}")
            print(f"  - Libros disponibles: {libros_disponibles}")
            print(f"  - Libros prestados: {libros_prestados_count}")
            print(f"  - Préstamos internos activos: {len(prestamos_activos_unicos)}")
            print(f"  - Préstamos externos activos: {len(prestamos_externos_unicos)}")
            print(f"  - Total préstamos activos: {len(prestamos_activos_unicos) + len(prestamos_externos_unicos)}")
            
            if len(prestamos_activos_unicos) + len(prestamos_externos_unicos) == libros_prestados_count:
                print("✅ ¡Perfecto! Los números coinciden ahora")
            else:
                print("⚠️  Aún hay inconsistencias en la base de datos")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al limpiar préstamos duplicados: {str(e)}")

if __name__ == '__main__':
    limpiar_prestamos_duplicados() 