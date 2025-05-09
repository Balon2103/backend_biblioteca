from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.usuario import Usuario
from app.utils.decorators import login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"Intento de inicio de sesión - Usuario: {username}")  # Debug
        
        user = Usuario.query.filter_by(username=username).first()
        if user:
            print(f"Usuario encontrado: {user.username}")  # Debug
            if user.check_password(password):
                print("Contraseña correcta")  # Debug
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('admin.index'))
            else:
                print("Contraseña incorrecta")  # Debug
        else:
            print("Usuario no encontrado")  # Debug
        
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
    
    return render_template('auth/registro.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('main.index')) 