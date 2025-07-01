from flask import current_app, url_for, render_template
from flask_mail import Message
from threading import Thread
from config.email_config import mail
import logging

def send_async_email(app, msg):
    """Enviar correo de forma asíncrona"""
    with app.app_context():
        try:
            print(f"🚀 RENDER DEBUG: Intentando enviar correo a {msg.recipients}")
            print(f"🚀 RENDER DEBUG: Configuración SMTP: {app.config.get('MAIL_SERVER')}:{app.config.get('MAIL_PORT')}")
            print(f"🚀 RENDER DEBUG: Usuario SMTP: {app.config.get('MAIL_USERNAME')}")
            print(f"🚀 RENDER DEBUG: Suprimir envío: {app.config.get('MAIL_SUPPRESS_SEND')}")
            
            mail.send(msg)
            print(f"✅ RENDER DEBUG: Correo enviado exitosamente a {msg.recipients}")
            logging.info(f"Correo enviado exitosamente a {msg.recipients}")
        except Exception as e:
            print(f"❌ RENDER DEBUG: Error al enviar correo: {str(e)}")
            logging.error(f"Error al enviar correo: {str(e)}")

def send_email(subject, recipients, template, **kwargs):
    """Enviar correo electrónico usando una plantilla"""
    try:
        # Limpiar el asunto de caracteres problemáticos SOLO si da error, pero intentamos UTF-8 primero
        msg = Message(
            subject=subject,
            recipients=recipients,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        # Renderizar el contenido del correo desde la plantilla
        html_content = render_template(f'emails/{template}.html', **kwargs)
        text_content = render_template(f'emails/{template}.txt', **kwargs)
        # Forzar a UTF-8 si es necesario
        if isinstance(html_content, str):
            html_content = html_content.encode('utf-8').decode('utf-8')
        if isinstance(text_content, str):
            text_content = text_content.encode('utf-8').decode('utf-8')
        msg.html = html_content
        msg.body = text_content
        # Configurar codificación UTF-8
        msg.charset = 'utf-8'
        # Enviar de forma asíncrona
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
        return True
    except Exception as e:
        logging.error(f"Error al preparar correo: {str(e)}")
        # Intentar enviar con asunto limpio si falla
        try:
            subject_clean = subject.encode('ascii', 'ignore').decode('ascii')
            msg = Message(
                subject=subject_clean,
                recipients=recipients,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            html_content = render_template(f'emails/{template}.html', **kwargs)
            text_content = render_template(f'emails/{template}.txt', **kwargs)
            msg.html = html_content.encode('utf-8').decode('utf-8')
            msg.body = text_content.encode('utf-8').decode('utf-8')
            msg.charset = 'utf-8'
            Thread(
                target=send_async_email,
                args=(current_app._get_current_object(), msg)
            ).start()
            return True
        except Exception as e2:
            logging.error(f"Error alternativo al preparar correo: {str(e2)}")
            return False

def send_password_reset_email(user):
    """Enviar correo de recuperación de contraseña"""
    print(f"🚀 RENDER DEBUG: Iniciando recuperación para usuario {user.email}")
    token = user.get_reset_token()
    # URL para restablecer contraseña
    reset_url = url_for('restablecer_contrasena', token=token, _external=True)
    print(f"🚀 RENDER DEBUG: URL de reset: {reset_url}")
    # Enviar correo
    result = send_email(
        subject='Recuperación de Contraseña - Sistema Bibliotecario',
        recipients=[user.email],
        template='password_reset',
        user=user,
        reset_url=reset_url
    )
    print(f"🚀 RENDER DEBUG: Resultado del envío: {result}")
    return result

def send_welcome_email(user):
    """Enviar correo de bienvenida a nuevos usuarios"""
    return send_email(
        subject='Bienvenido al Sistema Bibliotecario',
        recipients=[user.email],
        template='welcome',
        user=user
    ) 