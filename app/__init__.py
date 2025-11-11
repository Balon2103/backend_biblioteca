from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import config
import os

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Configuración de la base de datos
    if 'RENDER' in os.environ:
        # En producción (Render.com)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///biblioteca.db')
    else:
        # En desarrollo local
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
 # ⚙️ Agregar límite máximo permitido (por ejemplo, 50 MB)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

    # Aplicar configuración adicional
    app.config.from_object(config[config_name])

    # Inicializar SQLAlchemy con la app
    db.init_app(app)

    # Registrar blueprints
    from app.routes.main import main as main_blueprint
    from app.routes.auth import auth as auth_blueprint
    from app.routes.admin import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Registrar context processors
    from app.utils.helpers import formatear_valor
    app.context_processor(lambda: dict(formatear_valor=formatear_valor))

    # Importar modelos después de registrar los blueprints
    with app.app_context():
        # Importar modelos
        from app.models.usuario import Usuario
        from app.models.libro import Libro
        from app.models.prestamo import Prestamo, PersonaPrestamo
        
        # Crear tablas de la base de datos
        db.create_all()
        
        # Crear usuario administrador si no existe
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                email='admin@example.com',
                nombre='Administrador',
                apellido='Sistema',
                cedula='0000000000',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuario administrador creado")
        
        print("Base de datos inicializada correctamente")

    return app
