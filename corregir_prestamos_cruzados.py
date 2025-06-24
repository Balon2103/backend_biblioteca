from main import app, db
from models import Libro, Prestamo, PersonaPrestamo

def corregir_prestamos_cruzados():
    """Corrige automáticamente los préstamos cruzados eliminando los externos"""
    with app.app_context():
        try:
            print("🔧 Corrigiendo préstamos cruzados automáticamente...")
            
            # Obtener todos los préstamos activos
            prestamos_internos = Prestamo.query.filter_by(estado='activo').all()
            prestamos_externos = PersonaPrestamo.query.filter_by(estado='activo').all()
            
            # Crear sets de libros prestados
            libros_internos = set(p.libro_id for p in prestamos_internos)
            libros_externos = set(p.libro_id for p in prestamos_externos)
            
            # Encontrar libros con ambos tipos de préstamos
            libros_cruzados = libros_internos.intersection(libros_externos)
            
            print(f"📊 Préstamos internos activos: {len(prestamos_internos)}")
            print(f"📊 Préstamos externos activos: {len(prestamos_externos)}")
            print(f"📊 Libros con préstamos cruzados: {len(libros_cruzados)}")
            
            if libros_cruzados:
                print("\n🗑️  Eliminando préstamos externos duplicados...")
                prestamos_a_eliminar = []
                
                for libro_id in libros_cruzados:
                    libro = Libro.query.get(libro_id)
                    if libro:
                        print(f"  - Libro '{libro.titulo}' (ID: {libro_id})")
                        
                        # Obtener préstamos externos de este libro
                        prestamos_ext = [p for p in prestamos_externos if p.libro_id == libro_id]
                        for prestamo in prestamos_ext:
                            print(f"    * Eliminando préstamo externo ID {prestamo.id} - {prestamo.nombre} {prestamo.apellido}")
                            prestamos_a_eliminar.append(prestamo)
                
                # Eliminar los préstamos externos duplicados
                for prestamo in prestamos_a_eliminar:
                    db.session.delete(prestamo)
                
                db.session.commit()
                print(f"✅ {len(prestamos_a_eliminar)} préstamos externos eliminados")
                
                # Corregir disponibilidad de libros
                print("\n🔄 Corrigiendo disponibilidad de libros...")
                Libro.query.update({Libro.disponible: True})
                db.session.commit()
                
                # Obtener préstamos finales
                prestamos_finales = Prestamo.query.filter_by(estado='activo').all()
                prestamos_ext_finales = PersonaPrestamo.query.filter_by(estado='activo').all()
                
                libros_prestados = set()
                for p in prestamos_finales:
                    libros_prestados.add(p.libro_id)
                for p in prestamos_ext_finales:
                    libros_prestados.add(p.libro_id)
                
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
                
                print(f"\n📊 Estadísticas finales:")
                print(f"  - Total de libros: {total_libros}")
                print(f"  - Libros disponibles: {libros_disponibles}")
                print(f"  - Libros prestados: {libros_prestados_count}")
                print(f"  - Préstamos internos activos: {len(prestamos_finales)}")
                print(f"  - Préstamos externos activos: {len(prestamos_ext_finales)}")
                print(f"  - Total préstamos activos: {len(prestamos_finales) + len(prestamos_ext_finales)}")
                
                if len(prestamos_finales) + len(prestamos_ext_finales) == libros_prestados_count:
                    print("✅ ¡Perfecto! Los números coinciden ahora")
                    print("✅ Las estadísticas ahora son correctas")
                else:
                    print("⚠️  Aún hay inconsistencias en la base de datos")
            else:
                print("✅ No hay préstamos cruzados que corregir")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al corregir préstamos cruzados: {str(e)}")

if __name__ == '__main__':
    corregir_prestamos_cruzados() 