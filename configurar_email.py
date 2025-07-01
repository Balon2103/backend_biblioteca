#!/usr/bin/env python3
"""
Script interactivo para configurar el correo electrónico
"""

import os
import re

def validar_email(email):
    """Validar formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def configurar_email():
    """Configurar el correo electrónico interactivamente"""
    print("=== CONFIGURACIÓN DE CORREO ELECTRÓNICO ===")
    print("Este script te ayudará a configurar el envío de correos.")
    print()
    
    # Obtener configuración actual si existe
    config_actual = {}
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for linea in f:
                if '=' in linea and not linea.startswith('#'):
                    key, value = linea.strip().split('=', 1)
                    config_actual[key] = value
    
    print("Configuración actual:")
    print(f"  Servidor: {config_actual.get('MAIL_SERVER', 'No configurado')}")
    print(f"  Puerto: {config_actual.get('MAIL_PORT', 'No configurado')}")
    print(f"  Usuario: {config_actual.get('MAIL_USERNAME', 'No configurado')}")
    print(f"  Remitente: {config_actual.get('MAIL_DEFAULT_SENDER', 'No configurado')}")
    print(f"  Envío suprimido: {config_actual.get('MAIL_SUPPRESS_SEND', 'No configurado')}")
    print()
    
    # Preguntar si quiere cambiar la configuración
    cambiar = input("¿Quieres cambiar la configuración? (s/n): ").lower().strip()
    if cambiar != 's':
        print("Configuración no modificada.")
        return
    
    print()
    print("=== NUEVA CONFIGURACIÓN ===")
    
    # Configuración del servidor (Gmail por defecto)
    print("Configuración del servidor SMTP:")
    mail_server = input(f"Servidor SMTP (Enter para Gmail): ").strip() or "smtp.gmail.com"
    mail_port = input(f"Puerto (Enter para 587): ").strip() or "587"
    
    # Configuración de seguridad
    print()
    print("Configuración de seguridad:")
    use_tls = input("¿Usar TLS? (s/n, Enter para sí): ").lower().strip() or "s"
    use_ssl = input("¿Usar SSL? (s/n, Enter para no): ").lower().strip() or "n"
    
    # Credenciales
    print()
    print("Credenciales de Gmail:")
    print("IMPORTANTE: Necesitas una contraseña de aplicación de Gmail.")
    print("1. Ve a tu cuenta de Google")
    print("2. Seguridad > Verificación en dos pasos (actívala si no está)")
    print("3. Contraseñas de aplicación > Generar nueva contraseña")
    print("4. Usa esa contraseña aquí, NO tu contraseña normal de Gmail")
    print()
    
    mail_username = input("Correo de Gmail: ").strip()
    while not validar_email(mail_username):
        print("❌ Formato de correo inválido")
        mail_username = input("Correo de Gmail: ").strip()
    
    mail_password = input("Contraseña de aplicación: ").strip()
    while not mail_password:
        print("❌ La contraseña no puede estar vacía")
        mail_password = input("Contraseña de aplicación: ").strip()
    
    # Remitente
    mail_sender = input(f"Remitente (Enter para usar {mail_username}): ").strip() or mail_username
    
    # Habilitar envío real
    print()
    print("¿Quieres habilitar el envío real de correos?")
    print("  - s: Sí, enviar correos reales")
    print("  - n: No, mantener en modo prueba (no se envían)")
    suppress_send = input("Opción (s/n): ").lower().strip()
    
    # Crear archivo .env
    env_content = f"""# Configuración del Sistema Bibliotecario
SECRET_KEY=mi_clave_secreta_super_segura_2025

# Configuración de correo electrónico
MAIL_SERVER={mail_server}
MAIL_PORT={mail_port}
MAIL_USE_TLS={'True' if use_tls == 's' else 'False'}
MAIL_USE_SSL={'True' if use_ssl == 's' else 'False'}
MAIL_USERNAME={mail_username}
MAIL_PASSWORD={mail_password}
MAIL_DEFAULT_SENDER={mail_sender}

# Configuración de envío de correos
MAIL_SUPPRESS_SEND={'False' if suppress_send == 's' else 'True'}

# Configuración de la aplicación
SERVER_NAME=localhost:5000
APPLICATION_ROOT=/
PREFERRED_URL_SCHEME=http
"""
    
    # Guardar archivo
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print()
    print("✅ Configuración guardada en .env")
    print()
    print("Resumen de la configuración:")
    print(f"  Servidor: {mail_server}:{mail_port}")
    print(f"  Usuario: {mail_username}")
    print(f"  Remitente: {mail_sender}")
    print(f"  TLS: {'Sí' if use_tls == 's' else 'No'}")
    print(f"  SSL: {'Sí' if use_ssl == 's' else 'No'}")
    print(f"  Envío real: {'Sí' if suppress_send == 's' else 'No'}")
    print()
    
    if suppress_send == 's':
        print("🎉 ¡El envío de correos está habilitado!")
        print("Ahora puedes probar la recuperación de contraseña.")
    else:
        print("⚠️  El envío de correos está deshabilitado (modo prueba)")
        print("Los correos no se enviarán realmente.")

if __name__ == "__main__":
    configurar_email() 