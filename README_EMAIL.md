# Configuración del Sistema de Correos Electrónicos

Este documento explica cómo configurar el sistema de correos electrónicos para el Sistema Bibliotecario.

## Funcionalidades Implementadas

- ✅ **Recuperación de contraseña**: Envío de correos con enlaces seguros para restablecer contraseñas
- ✅ **Correos de bienvenida**: Notificación automática cuando se registra un nuevo usuario
- ✅ **Envío asíncrono**: Los correos se envían en segundo plano sin bloquear la aplicación
- ✅ **Plantillas HTML y texto**: Soporte para correos con formato HTML y versión de texto plano
- ✅ **Tokens seguros**: Enlaces de recuperación con expiración automática (30 minutos)

## Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente configuración:

```env
# Clave secreta de la aplicación
SECRET_KEY=tu_clave_secreta_muy_segura_aqui

# Configuración de correo electrónico
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
MAIL_DEFAULT_SENDER=tu_correo@gmail.com

# Para desarrollo, puedes deshabilitar el envío de correos
# MAIL_SUPPRESS_SEND=True
```

### 3. Configurar Gmail (Recomendado)

#### Paso 1: Habilitar verificación en dos pasos
1. Ve a tu cuenta de Google
2. Activa la verificación en dos pasos

#### Paso 2: Generar contraseña de aplicación
1. Ve a "Seguridad" en tu cuenta de Google
2. Busca "Contraseñas de aplicación"
3. Genera una nueva contraseña para "Correo"
4. Usa esta contraseña en `MAIL_PASSWORD`

### 4. Configurar otros proveedores

#### Outlook/Hotmail
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

#### Yahoo
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

## Uso

### Recuperación de Contraseña

1. El usuario hace clic en "¿Olvidaste tu contraseña?" en la página de login
2. Ingresa su correo electrónico
3. El sistema envía un correo con un enlace seguro
4. El usuario hace clic en el enlace y establece una nueva contraseña
5. El enlace expira automáticamente en 30 minutos

### Correos de Bienvenida

Los correos de bienvenida se envían automáticamente cuando:
- Un superadmin registra un nuevo usuario
- El usuario recibe información sobre su cuenta y funcionalidades disponibles

## Pruebas

### Probar el sistema de correos

```bash
python test_email.py
```

Este script probará el envío de correos de recuperación y bienvenida.

### Modo de desarrollo

Para desarrollo, puedes deshabilitar el envío real de correos:

```env
MAIL_SUPPRESS_SEND=True
```

## Estructura de archivos

```
├── config/
│   └── email_config.py          # Configuración del correo
├── utils/
│   └── email_service.py         # Servicio de envío de correos
├── templates/
│   └── emails/
│       ├── password_reset.html  # Plantilla HTML recuperación
│       ├── password_reset.txt   # Plantilla texto recuperación
│       ├── welcome.html         # Plantilla HTML bienvenida
│       └── welcome.txt          # Plantilla texto bienvenida
├── test_email.py                # Script de pruebas
└── env_example.txt              # Ejemplo de configuración
```

## Seguridad

- Los tokens de recuperación expiran en 30 minutos
- Los enlaces son únicos y no reutilizables
- Se usa `itsdangerous` para generar tokens seguros
- Los correos se envían de forma asíncrona para no bloquear la aplicación

## Solución de problemas

### Error: "Authentication failed"
- Verifica que la verificación en dos pasos esté activada
- Usa una contraseña de aplicación, no tu contraseña normal
- Verifica que `MAIL_USERNAME` y `MAIL_PASSWORD` sean correctos

### Error: "Connection refused"
- Verifica que `MAIL_SERVER` y `MAIL_PORT` sean correctos
- Asegúrate de que `MAIL_USE_TLS` esté configurado correctamente

### Los correos no se envían
- Verifica que `MAIL_SUPPRESS_SEND` no esté en `True`
- Revisa los logs de la aplicación para errores
- Ejecuta `python test_email.py` para diagnosticar

## Personalización

### Modificar plantillas

Las plantillas están en `templates/emails/` y puedes personalizarlas:
- `password_reset.html`: Correo de recuperación de contraseña
- `welcome.html`: Correo de bienvenida

### Agregar nuevos tipos de correo

1. Crea las plantillas HTML y TXT en `templates/emails/`
2. Agrega la función en `utils/email_service.py`
3. Llama a la función desde donde necesites enviar el correo

## Soporte

Si tienes problemas con la configuración:
1. Revisa los logs de la aplicación
2. Ejecuta el script de pruebas
3. Verifica la configuración de tu proveedor de correo
4. Contacta al administrador del sistema 