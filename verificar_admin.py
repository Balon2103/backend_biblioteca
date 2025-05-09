from app import db
from app.models.usuario import Usuario

# Buscar el usuario administrador
admin = Usuario.query.filter_by(username='admin').first()

if admin:
    print("Usuario administrador encontrado:")
    print(f"ID: {admin.id}")
    print(f"Username: {admin.username}")
    print(f"Email: {admin.email}")
    print(f"Nombre: {admin.nombre}")
    print(f"Apellido: {admin.apellido}")
    print(f"Cédula: {admin.cedula}")
    print(f"Es admin: {admin.is_admin}")
else:
    print("No se encontró el usuario administrador") 