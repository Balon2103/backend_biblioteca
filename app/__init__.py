from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import config

db = SQLAlchemy()  # ❗️ Solo se instancia, no se pasa ningún app aquí

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

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
        print("Base de datos inicializada correctamente")

    return app
