from main import app, db
from models import Libro, Usuario, Prestamo, PersonaPrestamo, Miembro
from datetime import datetime, timedelta
import random

def crear_datos_estadisticas():
    """Crea datos de prueba para las estadísticas"""
    with app.app_context():
        try:
            print("🔄 Creando datos de prueba para estadísticas...")
            
            # Obtener algunos libros existentes
            libros = Libro.query.limit(20).all()
            if not libros:
                print("❌ No hay libros en la base de datos. Primero agrega algunos libros.")
                return
            
            # Obtener usuarios existentes
            usuarios = Usuario.query.filter_by(is_admin=False).all()
            if not usuarios:
                print("❌ No hay usuarios en la base de datos. Primero crea algunos usuarios.")
                return
            
            # Obtener miembros existentes
            miembros = Miembro.query.all()
            if not miembros:
                print("❌ No hay miembros en la base de datos. Primero crea algunos miembros.")
                return
            
            print(f"📚 Libros disponibles: {len(libros)}")
            print(f"👥 Usuarios disponibles: {len(usuarios)}")
            print(f"👤 Miembros disponibles: {len(miembros)}")
            
            # Crear préstamos internos de los últimos 6 meses
            print("\n📖 Creando préstamos internos...")
            for i in range(50):  # 50 préstamos internos
                # Fecha aleatoria en los últimos 6 meses
                dias_atras = random.randint(1, 180)
                fecha_prestamo = datetime.utcnow() - timedelta(days=dias_atras)
                fecha_devolucion = fecha_prestamo + timedelta(days=15)
                
                # 70% de probabilidad de que esté devuelto
                if random.random() < 0.7:
                    estado = 'devuelto'
                    fecha_devolucion_real = fecha_devolucion + timedelta(days=random.randint(-5, 10))
                else:
                    estado = 'activo'
                    fecha_devolucion_real = None
                
                prestamo = Prestamo(
                    usuario_id=random.choice(usuarios).id,
                    libro_id=random.choice(libros).id,
                    fecha_prestamo=fecha_prestamo,
                    fecha_devolucion_esperada=fecha_devolucion,
                    fecha_devolucion_real=fecha_devolucion_real,
                    estado=estado
                )
                db.session.add(prestamo)
            
            # Crear préstamos externos de los últimos 6 meses
            print("📖 Creando préstamos externos...")
            nombres_ejemplo = [
                ("Juan", "Pérez"), ("María", "García"), ("Carlos", "López"),
                ("Ana", "Martínez"), ("Luis", "Rodríguez"), ("Carmen", "González"),
                ("Pedro", "Fernández"), ("Isabel", "Moreno"), ("Miguel", "Jiménez"),
                ("Rosa", "Ruiz"), ("Francisco", "Díaz"), ("Elena", "Serrano"),
                ("Javier", "Sánchez"), ("Teresa", "Ramírez"), ("Antonio", "Torres")
            ]
            
            for i in range(30):  # 30 préstamos externos
                # Fecha aleatoria en los últimos 6 meses
                dias_atras = random.randint(1, 180)
                fecha_prestamo = datetime.utcnow() - timedelta(days=dias_atras)
                fecha_devolucion = fecha_prestamo + timedelta(days=15)
                
                # 60% de probabilidad de que esté devuelto
                if random.random() < 0.6:
                    estado = 'devuelto'
                    fecha_devolucion_real = fecha_devolucion + timedelta(days=random.randint(-3, 8))
                else:
                    estado = 'activo'
                    fecha_devolucion_real = None
                
                nombre, apellido = random.choice(nombres_ejemplo)
                
                prestamo_externo = PersonaPrestamo(
                    nombre=nombre,
                    apellido=apellido,
                    cedula=f"{random.randint(10000000, 99999999)}",
                    direccion=f"Calle {random.randint(1, 100)} # {random.randint(1, 50)}",
                    telefono=f"0{random.randint(300000000, 399999999)}",
                    email=f"{nombre.lower()}.{apellido.lower()}@email.com",
                    observaciones="Préstamo externo de prueba",
                    libro_id=random.choice(libros).id,
                    fecha_prestamo=fecha_prestamo,
                    fecha_devolucion_esperada=fecha_devolucion,
                    fecha_devolucion_real=fecha_devolucion_real,
                    estado=estado
                )
                db.session.add(prestamo_externo)
            
            # Crear algunos préstamos para miembros específicos (para el ranking)
            print("👤 Creando préstamos para miembros...")
            for miembro in miembros[:5]:  # Top 5 miembros
                num_prestamos = random.randint(3, 8)  # Entre 3 y 8 préstamos por miembro
                for j in range(num_prestamos):
                    dias_atras = random.randint(1, 120)
                    fecha_prestamo = datetime.utcnow() - timedelta(days=dias_atras)
                    fecha_devolucion = fecha_prestamo + timedelta(days=15)
                    
                    if random.random() < 0.8:
                        estado = 'devuelto'
                        fecha_devolucion_real = fecha_devolucion + timedelta(days=random.randint(-2, 5))
                    else:
                        estado = 'activo'
                        fecha_devolucion_real = None
                    
                    prestamo_miembro = Prestamo(
                        usuario_id=miembro.id,  # Asumiendo que los miembros son usuarios
                        libro_id=random.choice(libros).id,
                        fecha_prestamo=fecha_prestamo,
                        fecha_devolucion_esperada=fecha_devolucion,
                        fecha_devolucion_real=fecha_devolucion_real,
                        estado=estado
                    )
                    db.session.add(prestamo_miembro)
            
            # Crear préstamos para libros específicos (para el ranking)
            print("📚 Creando préstamos para libros populares...")
            libros_populares = libros[:5]  # Top 5 libros
            for libro in libros_populares:
                num_prestamos = random.randint(5, 12)  # Entre 5 y 12 préstamos por libro
                for k in range(num_prestamos):
                    dias_atras = random.randint(1, 150)
                    fecha_prestamo = datetime.utcnow() - timedelta(days=dias_atras)
                    fecha_devolucion = fecha_prestamo + timedelta(days=15)
                    
                    if random.random() < 0.75:
                        estado = 'devuelto'
                        fecha_devolucion_real = fecha_devolucion + timedelta(days=random.randint(-3, 7))
                    else:
                        estado = 'activo'
                        fecha_devolucion_real = None
                    
                    prestamo_libro = Prestamo(
                        usuario_id=random.choice(usuarios).id,
                        libro_id=libro.id,
                        fecha_prestamo=fecha_prestamo,
                        fecha_devolucion_esperada=fecha_devolucion,
                        fecha_devolucion_real=fecha_devolucion_real,
                        estado=estado
                    )
                    db.session.add(prestamo_libro)
            
            # Actualizar disponibilidad de libros
            print("🔄 Actualizando disponibilidad de libros...")
            prestamos_activos = Prestamo.query.filter_by(estado='activo').all()
            prestamos_externos_activos = PersonaPrestamo.query.filter_by(estado='activo').all()
            
            libros_prestados = set()
            for prestamo in prestamos_activos:
                libros_prestados.add(prestamo.libro_id)
            for prestamo in prestamos_externos_activos:
                libros_prestados.add(prestamo.libro_id)
            
            # Marcar libros como no disponibles si están prestados
            for libro_id in libros_prestados:
                libro = Libro.query.get(libro_id)
                if libro:
                    libro.disponible = False
            
            db.session.commit()
            
            print("✅ Datos de prueba creados exitosamente!")
            print(f"📊 Total de préstamos internos: {Prestamo.query.count()}")
            print(f"📊 Total de préstamos externos: {PersonaPrestamo.query.count()}")
            print(f"📊 Préstamos activos: {Prestamo.query.filter_by(estado='activo').count() + PersonaPrestamo.query.filter_by(estado='activo').count()}")
            print(f"📊 Préstamos devueltos: {Prestamo.query.filter_by(estado='devuelto').count() + PersonaPrestamo.query.filter_by(estado='devuelto').count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear datos de prueba: {str(e)}")

if __name__ == '__main__':
    crear_datos_estadisticas() 