from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.usuario import Usuario
from app.utils.decorators import login_required
import logging

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        logging.info(f"Intento de inicio de sesión - Usuario: {username}")
        
        if not username or not password:
            flash('Por favor ingrese usuario y contraseña', 'danger')
            return render_template('auth/login.html')
        
        user = Usuario.query.filter_by(username=username).first()
        if user:
            logging.info(f"Usuario encontrado: {user.username}")
            if user.check_password(password):
                logging.info("Contraseña correcta")
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('admin.index'))
            else:
                logging.warning("Contraseña incorrecta")
        else:
            logging.warning("Usuario no encontrado")
        
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        
        if not all([username, email, password, confirm_password, nombre, apellido, cedula]):
            flash('Por favor complete todos los campos obligatorios', 'danger')
            return redirect(url_for('auth.registro'))
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.registro'))
        
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('auth.registro'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('auth.registro'))
        
        if Usuario.query.filter_by(cedula=cedula).first():
            flash('La cédula ya está registrada', 'danger')
            return redirect(url_for('auth.registro'))
        
        try:
            user = Usuario(
                username=username,
                email=email,
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                telefono=telefono
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registro exitoso. Por favor inicie sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error en el registro: {str(e)}")
            flash('Error al registrar usuario. Por favor intente nuevamente.', 'danger')
            return redirect(url_for('auth.registro'))
    
    return render_template('auth/registro.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('main.index')) 