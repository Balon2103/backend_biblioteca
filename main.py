from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
from extensions import db
from models import Libro, Usuario, Prestamo, PersonaPrestamo
import os
from datetime import datetime, timedelta
# import pdfkit  # Comentado temporalmente
from io import BytesIO
from sqlalchemy import or_

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Crear las tablas al iniciar la aplicación
with app.app_context():
    db.create_all()
    print("Base de datos inicializada correctamente")

LIBROS_POR_PAGINA = 10

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicie sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicie sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        user = db.session.get(Usuario, session['user_id'])
        if not user or not user.is_admin:
            flash('No tiene permisos para acceder a esta página', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def formatear_valor(valor):
    if pd.isna(valor) or valor is None or valor == '':
        return 'No disponible'
    return str(valor)

@app.context_processor
def utility_processor():
    return dict(formatear_valor=formatear_valor)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    query = request.args.get('q', '')
    
    if query:
        libros = Libro.query.filter(
            or_(
                Libro.titulo.ilike(f'%{query}%'),
                Libro.autor.ilike(f'%{query}%'),
                Libro.editorial.ilike(f'%{query}%'),
                Libro.materias.ilike(f'%{query}%')
            )
        ).paginate(page=page, per_page=per_page)
    else:
        libros = Libro.query.paginate(page=page, per_page=per_page)
    
    # Obtener todas las materias únicas para el filtro
    materias = db.session.query(Libro.materias).distinct().all()
    materias = [m[0] for m in materias if m[0]]  # Filtrar valores None
    
    return render_template('index.html', libros=libros, query=query, materias=materias)

@app.route('/libro/<int:id>')
def detalle_libro(id):
    libro = Libro.query.get_or_404(id)
    return render_template('detalle_libro.html', libro=libro)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin  # Guardar el estado de administrador
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin'))
        
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
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
            return redirect(url_for('registro'))
        
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('registro'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('registro'))
        
        if Usuario.query.filter_by(cedula=cedula).first():
            flash('La cédula ya está registrada', 'danger')
            return redirect(url_for('registro'))
        
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
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Usuario.query.filter_by(email=email).first()
        
        if user:
            # Aquí se implementaría la lógica para enviar el correo de recuperación
            # Por ahora solo mostraremos un mensaje
            flash('Si el correo existe en nuestra base de datos, recibirás instrucciones para recuperar tu contraseña.', 'info')
        else:
            # Por seguridad, mostramos el mismo mensaje aunque el correo no exista
            flash('Si el correo existe en nuestra base de datos, recibirás instrucciones para recuperar tu contraseña.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('recuperar_password.html')

@app.route('/restablecer-contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    user = Usuario.verify_reset_token(token)
    if not user:
        flash('El enlace de recuperación es inválido o ha expirado', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('restablecer_contrasena', token=token))
        
        user.set_password(password)
        db.session.commit()
        flash('Tu contraseña ha sido actualizada. Por favor inicia sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = request.args.get('q', '')
    
    if query:
        libros = Libro.query.filter(
            (Libro.titulo.ilike(f'%{query}%')) |
            (Libro.autor.ilike(f'%{query}%')) |
            (Libro.editorial.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=per_page)
    else:
        libros = Libro.query.paginate(page=page, per_page=per_page)
    
    return render_template('admin/index.html', libros=libros, query=query)

@app.route('/admin/libro/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_libro():
    if request.method == 'POST':
        libro = Libro(
            titulo=request.form.get('titulo'),
            autor=request.form.get('autor'),
            cota=request.form.get('cota'),
            editorial=request.form.get('editorial'),
            anio_edicion=request.form.get('anio_edicion'),
            ciudad=request.form.get('ciudad'),
            coleccion=request.form.get('coleccion'),
            medidas=request.form.get('medidas'),
            num_paginas=request.form.get('num_paginas'),
            caract_formato=request.form.get('caract_formato'),
            cant_ejemplares=request.form.get('cant_ejemplares'),
            tomos=request.form.get('tomos'),
            verificacion=request.form.get('verificacion'),
            materias=request.form.get('materias')
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro agregado exitosamente', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/nuevo_libro.html')

@app.route('/admin/libro/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_libro(id):
    libro = Libro.query.get_or_404(id)
    if request.method == 'POST':
        libro.titulo = request.form.get('titulo')
        libro.autor = request.form.get('autor')
        libro.cota = request.form.get('cota')
        libro.editorial = request.form.get('editorial')
        libro.anio_edicion = request.form.get('anio_edicion')
        libro.ciudad = request.form.get('ciudad')
        libro.coleccion = request.form.get('coleccion')
        libro.medidas = request.form.get('medidas')
        libro.num_paginas = request.form.get('num_paginas')
        libro.caract_formato = request.form.get('caract_formato')
        libro.cant_ejemplares = request.form.get('cant_ejemplares')
        libro.tomos = request.form.get('tomos')
        libro.verificacion = request.form.get('verificacion')
        libro.materias = request.form.get('materias')
        
        db.session.commit()
        flash('Libro actualizado exitosamente', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/editar_libro.html', libro=libro)

@app.route('/admin/libro/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado exitosamente', 'success')
    return redirect(url_for('admin'))

@app.route('/api/libros')
def api_libros():
    search = request.args.get('search', '')
    libros = Libro.query.filter(
        (Libro.titulo.ilike(f'%{search}%')) |
        (Libro.autor.ilike(f'%{search}%')) |
        (Libro.editorial.ilike(f'%{search}%'))
    ).limit(10).all()
    
    return jsonify([{
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'editorial': libro.editorial,
        'cota': libro.cota
    } for libro in libros])

@app.route('/prestamo/nuevo/<int:libro_id>', methods=['GET', 'POST'])
@login_required
def nuevo_prestamo(libro_id):
    try:
        libro = Libro.query.get_or_404(libro_id)
        
        if not libro.disponible:
            flash('Este libro no está disponible actualmente', 'danger')
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            usuario = Usuario.query.get(session['user_id'])
            fecha_prestamo = datetime.utcnow()
            fecha_devolucion = fecha_prestamo + timedelta(days=15)
            
            # Verificar nuevamente que el libro esté disponible
            if not libro.disponible:
                flash('Este libro ya no está disponible', 'danger')
                return redirect(url_for('index'))
            
            prestamo = Prestamo(
                usuario_id=usuario.id,
                libro_id=libro.id,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion_esperada=fecha_devolucion,
                estado='activo'
            )
            
            # Marcar el libro como no disponible
            libro.disponible = False
            
            db.session.add(prestamo)
            db.session.commit()
            
            flash('Préstamo registrado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        
        return render_template('nuevo_prestamo.html', libro=libro)
    except Exception as e:
        print(f"Error en nuevo préstamo: {str(e)}")
        db.session.rollback()
        flash('Error al procesar el préstamo', 'danger')
        return redirect(url_for('index'))

@app.route('/prestamo/devolver/<int:prestamo_id>', methods=['POST'])
@login_required
def devolver_libro(prestamo_id):
    try:
        prestamo = Prestamo.query.get_or_404(prestamo_id)
        
        # Verificar que el préstamo pertenece al usuario actual o es administrador
        if prestamo.usuario_id != session['user_id'] and not Usuario.query.get(session['user_id']).is_admin:
            flash('No tiene permiso para realizar esta acción', 'danger')
            return redirect(url_for('prestamos'))
        
        # Verificar que el préstamo no ha sido devuelto
        if prestamo.fecha_devolucion_real is None:
            # Actualizar el préstamo
            prestamo.fecha_devolucion_real = datetime.utcnow()
            prestamo.estado = 'devuelto'
            
            # Marcar el libro como disponible
            prestamo.libro.disponible = True
            
            db.session.commit()
            flash('Libro devuelto exitosamente', 'success')
        else:
            flash('Este libro ya ha sido devuelto', 'warning')
    except Exception as e:
        print(f"Error al devolver libro: {str(e)}")
        db.session.rollback()
        flash('Error al devolver el libro', 'danger')
    
    return redirect(url_for('prestamos'))

@app.route('/libro/<int:id>/ficha')
def ficha_bibliografica(id):
    libro = Libro.query.get_or_404(id)
    return render_template('ficha_bibliografica.html', libro=libro)

@app.route('/libro/<int:id>/ficha/pdf')
def ficha_bibliografica_pdf(id):
    # Temporalmente, redirigimos a la vista normal
    return redirect(url_for('ficha_bibliografica', id=id))

@app.route('/prestamo/externo/<int:libro_id>', methods=['GET', 'POST'])
def nuevo_prestamo_externo(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    
    if not libro.disponible:
        flash('Este libro no está disponible para préstamo', 'warning')
        return redirect(url_for('detalle_libro', id=libro.id))
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            cedula = request.form.get('cedula')
            direccion = request.form.get('direccion')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            observaciones = request.form.get('observaciones')
            
            # Validar campos requeridos
            if not all([nombre, apellido, cedula, direccion, telefono, email]):
                flash('Todos los campos marcados con * son obligatorios', 'danger')
                return redirect(request.url)
            
            # Crear nuevo préstamo externo
            fecha_prestamo = datetime.utcnow()
            fecha_devolucion = fecha_prestamo + timedelta(days=15)  # 15 días por defecto
            
            prestamo = PersonaPrestamo(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                direccion=direccion,
                telefono=telefono,
                email=email,
                observaciones=observaciones,
                libro_id=libro.id,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion_esperada=fecha_devolucion,
                estado='activo'
            )
            
            # Marcar libro como no disponible
            libro.disponible = False
            
            db.session.add(prestamo)
            db.session.commit()
            
            flash('Préstamo registrado exitosamente.', 'success')
            return redirect(url_for('admin_prestamos'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar préstamo externo: {str(e)}")
            flash('Error al registrar el préstamo. Por favor, intente nuevamente.', 'danger')
            return redirect(request.url)

    return render_template('nuevo_prestamo_externo.html', 
                         libro=libro, 
                         fecha_prestamo=datetime.utcnow(), 
                         fecha_devolucion=datetime.utcnow() + timedelta(days=15))

@app.route('/admin/prestamos')
@admin_required
def admin_prestamos():
    try:
        # Obtener préstamos internos activos
        prestamos_internos = Prestamo.query.filter(
            Prestamo.estado == 'activo'
        ).join(Usuario).join(Libro).order_by(Prestamo.fecha_prestamo.desc()).all()
        
        # Obtener préstamos externos activos
        prestamos_externos = PersonaPrestamo.query.filter(
            PersonaPrestamo.estado == 'activo'
        ).join(Libro).order_by(PersonaPrestamo.fecha_prestamo.desc()).all()
        
        # Obtener historial de préstamos internos
        historial_internos = Prestamo.query.filter(
            Prestamo.estado == 'devuelto'
        ).join(Usuario).join(Libro).order_by(Prestamo.fecha_prestamo.desc()).all()
        
        # Obtener historial de préstamos externos
        historial_externos = PersonaPrestamo.query.filter(
            PersonaPrestamo.estado == 'devuelto'
        ).join(Libro).order_by(PersonaPrestamo.fecha_prestamo.desc()).all()
        
        # Verificar y corregir libros no disponibles sin préstamos activos
        libros_no_disponibles = Libro.query.filter_by(disponible=False).all()
        for libro in libros_no_disponibles:
            prestamo_activo = Prestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_externo_activo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            if not prestamo_activo and not prestamo_externo_activo:
                print(f"Corrigiendo libro no disponible sin préstamo activo: {libro.titulo}")
                libro.disponible = True
                db.session.commit()
        
        # Imprimir información de depuración
        print("Préstamos internos activos:", len(prestamos_internos))
        print("Préstamos externos activos:", len(prestamos_externos))
        print("Historial internos:", len(historial_internos))
        print("Historial externos:", len(historial_externos))
        
        now = datetime.utcnow()
        
        return render_template('admin/prestamos.html', 
                             prestamos_internos=prestamos_internos,
                             prestamos_externos=prestamos_externos,
                             historial_internos=historial_internos,
                             historial_externos=historial_externos,
                             now=now)
    except Exception as e:
        print(f"Error en la ruta de gestión de préstamos: {str(e)}")
        flash('Error al cargar los préstamos', 'danger')
        return redirect(url_for('admin'))

@app.route('/admin/prestamo/devolver/externo/<int:prestamo_id>', methods=['POST'])
@admin_required
def devolver_libro_externo(prestamo_id):
    try:
        prestamo = db.session.get(PersonaPrestamo, prestamo_id)
        if not prestamo:
            flash('Préstamo no encontrado', 'danger')
            return redirect(url_for('admin_prestamos'))
            
        if prestamo.estado == 'activo':
            prestamo.marcar_como_devuelto()
            db.session.commit()
            flash('Libro devuelto exitosamente', 'success')
        else:
            flash('Este libro ya ha sido devuelto', 'warning')
    except Exception as e:
        print(f"Error al devolver libro externo: {str(e)}")
        db.session.rollback()
        flash('Error al devolver el libro', 'danger')
    return redirect(url_for('admin_prestamos'))

@app.route('/admin/prestamo/nuevo/<int:libro_id>', methods=['GET', 'POST'])
@admin_required
def admin_nuevo_prestamo(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    usuarios = Usuario.query.filter_by(is_admin=False).all()
    
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        fecha_prestamo = datetime.utcnow()
        fecha_devolucion = fecha_prestamo + timedelta(days=15)
        
        prestamo = Prestamo(
            usuario_id=usuario_id,
            libro_id=libro.id,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion_esperada=fecha_devolucion,
            estado='activo'
        )
        
        libro.disponible = False
        db.session.add(prestamo)
        db.session.commit()
        
        flash('Préstamo registrado exitosamente', 'success')
        return redirect(url_for('admin_prestamos'))
    
    return render_template('admin/nuevo_prestamo.html', libro=libro, usuarios=usuarios)

@app.route('/api/prestamo/<int:prestamo_id>')
@admin_required
def get_prestamo_details(prestamo_id):
    tipo = request.args.get('tipo', 'Prestamo')
    
    try:
        if tipo == 'Prestamo':
            prestamo = Prestamo.query.get_or_404(prestamo_id)
            if not prestamo:
                return jsonify({'error': 'Préstamo no encontrado'}), 404
            
            # Imprimir datos para depuración
            print("Datos del préstamo interno:", {
                'nombre': prestamo.usuario.nombre,
                'apellido': prestamo.usuario.apellido,
                'cedula': prestamo.usuario.cedula,
                'telefono': prestamo.usuario.telefono,
                'email': prestamo.usuario.email
            })
            
            return jsonify({
                'nombre': prestamo.usuario.nombre,
                'apellido': prestamo.usuario.apellido,
                'cedula': prestamo.usuario.cedula,
                'telefono': prestamo.usuario.telefono,
                'email': prestamo.usuario.email
            })
        else:  # PersonaPrestamo
            prestamo = PersonaPrestamo.query.get_or_404(prestamo_id)
            if not prestamo:
                return jsonify({'error': 'Préstamo no encontrado'}), 404
            
            # Imprimir datos para depuración
            print("Datos del préstamo externo:", {
                'nombre': prestamo.nombre,
                'apellido': prestamo.apellido,
                'cedula': prestamo.cedula,
                'direccion': prestamo.direccion,
                'telefono': prestamo.telefono,
                'email': prestamo.email,
                'observaciones': prestamo.observaciones
            })
            
            return jsonify({
                'nombre': prestamo.nombre,
                'apellido': prestamo.apellido,
                'cedula': prestamo.cedula,
                'direccion': prestamo.direccion,
                'telefono': prestamo.telefono,
                'email': prestamo.email,
                'observaciones': prestamo.observaciones
            })
    except Exception as e:
        print(f"Error al obtener detalles del préstamo: {str(e)}")
        return jsonify({'error': f'Error al obtener los detalles del préstamo: {str(e)}'}), 500

@app.route('/prestamos/borrar-historial', methods=['POST'])
@admin_required
def borrar_historial_prestamos():
    try:
        # Borrar el historial de préstamos internos
        Prestamo.query.filter(
            Prestamo.estado == 'devuelto'
        ).delete()
        
        # Borrar el historial de préstamos externos
        PersonaPrestamo.query.filter(
            PersonaPrestamo.estado == 'devuelto'
        ).delete()
        
        db.session.commit()
        flash('Historial de préstamos borrado exitosamente', 'success')
    except Exception as e:
        print(f"Error al borrar historial de préstamos: {str(e)}")
        db.session.rollback()
        flash('Error al borrar el historial de préstamos', 'danger')
    
    return redirect(url_for('admin_prestamos'))

@app.route('/mis-prestamos')
@login_required
def mis_prestamos():
    try:
        # Obtener préstamos activos del usuario
        prestamos_activos = Prestamo.query.filter(
            Prestamo.usuario_id == session['user_id'],
            Prestamo.estado == 'activo'
        ).join(Libro).order_by(Prestamo.fecha_prestamo.desc()).all()
        
        # Obtener historial de préstamos del usuario
        historial = Prestamo.query.filter(
            Prestamo.usuario_id == session['user_id'],
            Prestamo.estado == 'devuelto'
        ).join(Libro).order_by(Prestamo.fecha_prestamo.desc()).all()
        
        return render_template('mis_prestamos.html', 
                             prestamos_activos=prestamos_activos,
                             historial=historial)
    except Exception as e:
        print(f"Error al cargar mis préstamos: {str(e)}")
        flash('Error al cargar tus préstamos', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)