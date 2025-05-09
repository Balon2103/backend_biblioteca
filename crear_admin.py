from app import app, db
from app.models.usuario import Usuario

with app.app_context():
    # Crear todas las tablas
    db.create_all()
    
    # Verificar si ya existe un usuario administrador
    admin = Usuario.query.filter_by(username='admin').first()
    if admin:
        print("El usuario administrador ya existe")
    else:
        # Crear el usuario administrador con todos los campos requeridos
        admin = Usuario(
            username='admin',
            nombre='Admin',
            apellido='Sistema',
            cedula='00000000',
            email='admin@admin.com',
            telefono='0000000000',
            is_admin=True
        )
        admin.set_password('admin123')  # Cambiar esta contraseña en producción
        
        # Guardar en la base de datos
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado exitosamente")
        print("Usuario: admin")
        print("Contraseña: admin123") 