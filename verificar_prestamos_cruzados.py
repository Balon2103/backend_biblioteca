from main import app, db
from models import Libro, Prestamo, PersonaPrestamo

def verificar_prestamos_cruzados():
    """Verifica si hay libros con préstamos internos y externos simultáneos"""
    with app.app_context():
        try:
            print("🔍 Verificando préstamos cruzados...")
            
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
            print(f"📊 Libros únicos con préstamos internos: {len(libros_internos)}")
            print(f"📊 Libros únicos con préstamos externos: {len(libros_externos)}")
            print(f"📊 Libros con ambos tipos de préstamos: {len(libros_cruzados)}")
            
            if libros_cruzados:
                print("\n⚠️  Libros con préstamos internos y externos simultáneos:")
                for libro_id in libros_cruzados:
                    libro = Libro.query.get(libro_id)
                    if libro:
                        print(f"  - Libro ID {libro_id}: '{libro.titulo}'")
                        
                        # Mostrar préstamos internos
                        prestamos_int = [p for p in prestamos_internos if p.libro_id == libro_id]
                        for p in prestamos_int:
                            print(f"    * Préstamo interno ID {p.id} - Usuario ID {p.usuario_id}")
                        
                        # Mostrar préstamos externos
                        prestamos_ext = [p for p in prestamos_externos if p.libro_id == libro_id]
                        for p in prestamos_ext:
                            print(f"    * Préstamo externo ID {p.id} - {p.nombre} {p.apellido}")
                
                print(f"\n📊 Total de libros únicos prestados: {len(libros_internos.union(libros_externos))}")
                print(f"📊 Total de préstamos activos: {len(prestamos_internos) + len(prestamos_externos)}")
                
                # Preguntar si quiere corregir
                print("\n¿Quieres eliminar los préstamos externos duplicados? (s/n): ", end="")
                respuesta = input().lower()
                
                if respuesta == 's':
                    print("🗑️  Eliminando préstamos externos duplicados...")
                    for libro_id in libros_cruzados:
                        prestamos_ext = [p for p in prestamos_externos if p.libro_id == libro_id]
                        for prestamo in prestamos_ext:
                            print(f"  - Eliminando préstamo externo ID {prestamo.id} del libro '{Libro.query.get(libro_id).titulo}'")
                            db.session.delete(prestamo)
                    
                    db.session.commit()
                    print("✅ Préstamos externos duplicados eliminados")
                    
                    # Corregir disponibilidad
                    print("\n🔄 Corrigiendo disponibilidad...")
                    Libro.query.update({Libro.disponible: True})
                    db.session.commit()
                    
                    prestamos_finales = Prestamo.query.filter_by(estado='activo').all()
                    prestamos_ext_finales = PersonaPrestamo.query.filter_by(estado='activo').all()
                    
                    libros_prestados = set()
                    for p in prestamos_finales:
                        libros_prestados.add(p.libro_id)
                    for p in prestamos_ext_finales:
                        libros_prestados.add(p.libro_id)
                    
                    for libro_id in libros_prestados:
                        libro = Libro.query.get(libro_id)
                        if libro:
                            libro.disponible = False
                    
                    db.session.commit()
                    
                    print(f"\n📊 Estadísticas finales:")
                    print(f"  - Préstamos internos activos: {len(prestamos_finales)}")
                    print(f"  - Préstamos externos activos: {len(prestamos_ext_finales)}")
                    print(f"  - Libros prestados: {len(libros_prestados)}")
                    
                    total_libros = Libro.query.count()
                    libros_disponibles = Libro.query.filter_by(disponible=True).count()
                    libros_prestados_count = Libro.query.filter_by(disponible=False).count()
                    
                    print(f"  - Total de libros: {total_libros}")
                    print(f"  - Libros disponibles: {libros_disponibles}")
                    print(f"  - Libros prestados: {libros_prestados_count}")
                    
                    if len(prestamos_finales) + len(prestamos_ext_finales) == libros_prestados_count:
                        print("✅ ¡Perfecto! Los números coinciden ahora")
                    else:
                        print("⚠️  Aún hay inconsistencias")
            else:
                print("✅ No hay libros con préstamos cruzados")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al verificar préstamos cruzados: {str(e)}")

if __name__ == '__main__':
    verificar_prestamos_cruzados() 