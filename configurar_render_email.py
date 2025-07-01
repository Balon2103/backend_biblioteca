#!/usr/bin/env python3
"""
Script para configurar el correo en Render
"""

import os
from dotenv import load_dotenv

def configurar_render_email():
    """Configurar variables de entorno para Render"""
    print("=== CONFIGURACIÓN DE CORREO PARA RENDER ===")
    print()
    
    # Verificar si estamos en Render
    if os.environ.get('RENDER'):
        print("✅ Detectado entorno Render")
    else:
        print("⚠️  No estás en Render (entorno local)")
    
    print()
    print("📧 VARIABLES DE ENTORNO NECESARIAS EN RENDER:")
    print()
    print("MAIL_SERVER=smtp.gmail.com")
    print("MAIL_PORT=587")
    print("MAIL_USE_TLS=True")
    print("MAIL_USE_SSL=False")
    print("MAIL_USERNAME=eserxzd@gmail.com")
    print("MAIL_PASSWORD=wuhrdllsblertdul")
    print("MAIL_DEFAULT_SENDER=eserxzd@gmail.com")
    print("MAIL_SUPPRESS_SEND=False")
    print("MAIL_DEFAULT_CHARSET=utf-8")
    print()
    
    print("🔧 CÓMO CONFIGURAR EN RENDER:")
    print("1. Ve a tu dashboard de Render")
    print("2. Selecciona tu servicio web")
    print("3. Ve a 'Environment'")
    print("4. Agrega las variables de entorno arriba")
    print("5. Guarda y redeploya")
    print()
    
    print("⚠️  IMPORTANTE:")
    print("- Asegúrate de que la contraseña de aplicación sea correcta")
    print("- La verificación en dos pasos debe estar activada en Gmail")
    print("- El correo debe ser el mismo que usaste localmente")
    print()
    
    print("🧪 PARA PROBAR EN RENDER:")
    print("1. Después de configurar las variables")
    print("2. Ve a tu aplicación en Render")
    print("3. Prueba la función de recuperación de contraseña")
    print("4. Revisa los logs de Render para errores")
    print()
    
    # Verificar configuración actual
    print("📋 CONFIGURACIÓN ACTUAL:")
    print(f"  MAIL_SERVER: {os.environ.get('MAIL_SERVER', 'No configurado')}")
    print(f"  MAIL_PORT: {os.environ.get('MAIL_PORT', 'No configurado')}")
    print(f"  MAIL_USERNAME: {os.environ.get('MAIL_USERNAME', 'No configurado')}")
    print(f"  MAIL_PASSWORD: {'Configurado' if os.environ.get('MAIL_PASSWORD') else 'No configurado'}")
    print(f"  MAIL_DEFAULT_SENDER: {os.environ.get('MAIL_DEFAULT_SENDER', 'No configurado')}")
    print(f"  MAIL_SUPPRESS_SEND: {os.environ.get('MAIL_SUPPRESS_SEND', 'No configurado')}")

if __name__ == "__main__":
    configurar_render_email() 