import os
from flask_mail import Mail

# Configuración de correo electrónico
MAIL_CONFIG = {
    'MAIL_SERVER': os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
    'MAIL_PORT': int(os.environ.get('MAIL_PORT', 587)),
    'MAIL_USE_TLS': os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true',
    'MAIL_USE_SSL': os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true',
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME', 'eserxzd@gmail.com'),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', 'wuhrdllsblertdul'),
    'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER', 'eserxzd@gmail.com'),
    'MAIL_MAX_EMAILS': int(os.environ.get('MAIL_MAX_EMAILS', 10)),
    'MAIL_ASCII_ATTACHMENTS': False,
    'MAIL_SUPPRESS_SEND': os.environ.get('MAIL_SUPPRESS_SEND', 'False').lower() == 'true',
    'MAIL_DEFAULT_CHARSET': 'utf-8'
}

# Inicializar Flask-Mail
mail = Mail()

def init_mail(app):
    """Inicializar Flask-Mail con la aplicación"""
    for key, value in MAIL_CONFIG.items():
        app.config[key] = value
    mail.init_app(app) 