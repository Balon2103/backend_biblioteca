from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
from extensions import db
from models import Libro, Usuario, Prestamo, PersonaPrestamo, Miembro, PrestamoInterno
import os
from datetime import datetime, timedelta
# import pdfkit  # Comentado temporalmente
from io import BytesIO
from sqlalchemy import or_
import json
import re

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
    
    # Verificar si existe el superadmin
    superadmin = Usuario.query.filter_by(username='superadmin').first()
    if not superadmin:
        superadmin = Usuario(
            username='superadmin',
            nombre='Super',
            apellido='Administrador',
            cedula='0000000000',
            email='superadmin@biblioteca.com',
            telefono='0000000000',
            rol='superadmin'
        )
        superadmin.set_password('superadmin123')
        db.session.add(superadmin)
    
    # Verificar si existe el admin
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            nombre='Admin',
            apellido='Sistema',
            cedula='0000000001',
            email='admin@biblioteca.com',
            telefono='0000000001',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    try:
        db.session.commit()
        print("Usuarios administradores actualizados correctamente")
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar usuarios: {str(e)}")

    # Importar libros desde el archivo JSON si existe
    # try:
    #     if os.path.exists('libros.json'):
    #         with open('libros.json', 'r', encoding='utf-8') as f:
    #             libros_data = json.load(f)
    #             
    #         # Verificar si ya existen libros
    #         if Libro.query.count() == 0:
    #             for libro_data in libros_data:
    #                 libro = Libro(**libro_data)
    #                 db.session.add(libro)
    #             db.session.commit()
    #             print(f"Se importaron {len(libros_data)} libros correctamente")
    # except Exception as e:
    #     print(f"Error al importar libros: {str(e)}")

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
        if not user or (not user.is_admin and not user.is_superadmin):
            flash('No tiene permisos para acceder a esta página', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicie sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        user = db.session.get(Usuario, session['user_id'])
        if not user or not user.is_superadmin:
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
    return render_template('bienvenida.html')

@app.route('/catalogo')
def catalogo():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    query = request.args.get('q', '')
    categoria = request.args.get('categoria', '')
    materia_busqueda = request.args.get('materia', '')
    
    # Construir la consulta base
    libros_query = Libro.query
    
    # Aplicar filtro de categoría si se especifica
    if categoria:
        libros_query = libros_query.filter(Libro.materias.ilike(f'%{categoria}%'))
    
    # Aplicar búsqueda por texto si se especifica
    if query:
        search_term = f'%{query}%'
        libros_query = libros_query.filter(
            or_(
                Libro.titulo.ilike(search_term),
                Libro.autor.ilike(search_term),
                Libro.editorial.ilike(search_term),
                Libro.cota.ilike(search_term),
                Libro.coleccion.ilike(search_term)
            )
        )
    
    # Aplicar búsqueda específica por materia si se especifica
    if materia_busqueda:
        materia_term = f'%{materia_busqueda}%'
        libros_query = libros_query.filter(Libro.materias.ilike(materia_term))
    
    # Ordenar por título
    libros_query = libros_query.order_by(Libro.titulo)
    
    # Paginar los resultados
    libros = libros_query.paginate(page=page, per_page=per_page)
    
    # Obtener todas las materias únicas para el filtro
    materias = db.session.query(Libro.materias).distinct().all()
    materias = [m[0] for m in materias if m[0]]  # Filtrar valores None
    materias.sort()  # Ordenar las materias alfabéticamente
    
    return render_template('index.html', libros=libros, query=query, categoria=categoria, materia_busqueda=materia_busqueda, materias=materias)

@app.route('/libro/<int:id>')
def detalle_libro(id):
    libro = Libro.query.get_or_404(id)
    # Obtener parámetros de la página anterior para el botón volver
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    categoria = request.args.get('categoria', '')
    materia_busqueda = request.args.get('materia', '')
    return render_template('detalle_libro.html', libro=libro, page=page, query=query, categoria=categoria, materia_busqueda=materia_busqueda)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin  # Guardar el estado de administrador
            session['rol'] = user.rol  # Guardar el rol del usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
@superadmin_required
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
        rol = request.form.get('rol', 'usuario')  # Por defecto es usuario
        
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
            telefono=telefono,
            rol=rol,
            is_admin=(rol in ['admin', 'superadmin'])
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Usuario registrado exitosamente.', 'success')
        return redirect(url_for('admin'))
    
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
        ).order_by(Libro.titulo).paginate(page=page, per_page=per_page)
    else:
        libros = Libro.query.order_by(Libro.titulo).paginate(page=page, per_page=per_page)
    
    return render_template('admin/index.html', libros=libros, query=query)

@app.route('/admin/libro/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_libro():
    if request.method == 'POST':
        try:
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
            
            # Manejar la portada si se subió
            if 'portada' in request.files:
                portada = request.files['portada']
                if portada and portada.filename != '':
                    # Crear directorio para portadas si no existe
                    upload_folder = os.path.join(app.static_folder, 'uploads', 'portadas')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Guardar nueva portada
                    titulo_limpio = limpiar_nombre_archivo(libro.titulo)
                    filename = f"portada_{titulo_limpio}_{portada.filename}"
                    portada_path = os.path.join(upload_folder, filename)
                    portada.save(portada_path)
                    libro.portada = f"uploads/portadas/{filename}"
            
            db.session.add(libro)
            db.session.commit()
            flash('Libro agregado exitosamente', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al agregar libro: {str(e)}")
            flash('Error al agregar el libro', 'danger')
            return redirect(request.url)
    return render_template('admin/nuevo_libro.html')

@app.route('/admin/libro/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_libro(id):
    libro = Libro.query.get_or_404(id)
    if request.method == 'POST':
        try:
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
            
            # Manejar nueva portada si se subió
            if 'portada' in request.files:
                portada = request.files['portada']
                if portada and portada.filename != '':
                    # Crear directorio para portadas si no existe
                    upload_folder = os.path.join(app.static_folder, 'uploads', 'portadas')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Eliminar portada anterior si existe
                    if libro.portada:
                        portada_anterior = os.path.join(app.static_folder, libro.portada)
                        if os.path.exists(portada_anterior):
                            os.remove(portada_anterior)
                    
                    # Guardar nueva portada
                    titulo_limpio = limpiar_nombre_archivo(libro.titulo)
                    filename = f"portada_{titulo_limpio}_{portada.filename}"
                    portada_path = os.path.join(upload_folder, filename)
                    portada.save(portada_path)
                    libro.portada = f"uploads/portadas/{filename}"
            
            # Manejar eliminación de portada si se marca el checkbox
            if request.form.get('eliminar_portada') == 'on':
                if libro.portada:
                    # Eliminar archivo físico
                    portada_path = os.path.join(app.static_folder, libro.portada)
                    if os.path.exists(portada_path):
                        os.remove(portada_path)
                    # Limpiar referencia en la base de datos
                    libro.portada = None
            
            db.session.commit()
            flash('Libro actualizado exitosamente', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar libro: {str(e)}")
            flash('Error al actualizar el libro', 'danger')
    return render_template('admin/editar_libro.html', libro=libro)

@app.route('/admin/libro/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    try:
        # Eliminar portada si existe
        if libro.portada:
            portada_path = os.path.join(app.static_folder, libro.portada)
            if os.path.exists(portada_path):
                os.remove(portada_path)
        
        db.session.delete(libro)
        db.session.commit()
        flash('Libro eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar libro: {str(e)}")
        flash('Error al eliminar el libro', 'danger')
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
            return redirect(url_for('mis_prestamos'))
        
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
            return redirect(url_for('mis_prestamos'))
        
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
    
    return redirect(url_for('mis_prestamos'))

@app.route('/libro/<int:id>/ficha')
def ficha_bibliografica(id):
    libro = Libro.query.get_or_404(id)
    return render_template('ficha_bibliografica.html', libro=libro)

@app.route('/libro/<int:id>/ficha-compacta')
def ficha_bibliografica_compacta(id):
    libro = Libro.query.get_or_404(id)
    return render_template('ficha_compacta.html', libro=libro)

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
            institucion = request.form.get('institucion')
            cargo = request.form.get('cargo')
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
                institucion=institucion,
                cargo=cargo,
                observaciones=observaciones,
                tipo_prestamo='externo',
                libro_id=libro.id,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion_esperada=fecha_devolucion,
                estado='activo'
            )
            
            # Marcar libro como no disponible
            libro.disponible = False
            
            db.session.add(prestamo)
            db.session.commit()
            
            flash('Préstamo externo registrado exitosamente.', 'success')
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

@app.route('/prestamo/interno/<int:libro_id>', methods=['GET', 'POST'])
@admin_required
def nuevo_prestamo_interno(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    miembros = Miembro.query.filter_by(estado='activo').order_by(Miembro.apellidos).all()
    
    if not libro.disponible:
        flash('Este libro no está disponible para préstamo', 'warning')
        return redirect(url_for('detalle_libro', id=libro.id))
    
    if request.method == 'POST':
        try:
            miembro_id = request.form.get('miembro_id')
            
            if not miembro_id:
                flash('Debe seleccionar un miembro', 'danger')
                return redirect(request.url)
            
            miembro = Miembro.query.get_or_404(miembro_id)
            
            # Crear nuevo préstamo interno usando el modelo PrestamoInterno
            fecha_prestamo = datetime.utcnow()
            fecha_devolucion = fecha_prestamo + timedelta(days=15)  # 15 días para internos
            
            prestamo = PrestamoInterno(
                miembro_id=miembro.id,
                libro_id=libro.id,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion_esperada=fecha_devolucion,
                estado='activo'
            )
            
            # Marcar libro como no disponible
            libro.disponible = False
            
            db.session.add(prestamo)
            db.session.commit()
            
            flash(f'Préstamo interno registrado exitosamente para {miembro.nombre_completo}.', 'success')
            return redirect(url_for('admin_prestamos'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar préstamo interno: {str(e)}")
            flash('Error al registrar el préstamo. Por favor, intente nuevamente.', 'danger')
            return redirect(request.url)

    return render_template('admin/nuevo_prestamo_interno.html', 
                         libro=libro, 
                         miembros=miembros,
                         fecha_prestamo=datetime.utcnow(), 
                         fecha_devolucion=datetime.utcnow() + timedelta(days=15))

@app.route('/seleccionar-tipo-prestamo/<int:libro_id>')
@admin_required
def seleccionar_tipo_prestamo(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    
    if not libro.disponible:
        flash('Este libro no está disponible para préstamo', 'warning')
        return redirect(url_for('detalle_libro', id=libro.id))
    
    return render_template('seleccionar_tipo_prestamo.html', libro=libro)

@app.route('/admin/prestamos')
@admin_required
def admin_prestamos():
    try:
        # Obtener préstamos internos activos (del modelo PrestamoInterno)
        prestamos_internos = PrestamoInterno.query.filter(
            PrestamoInterno.estado == 'activo'
        ).join(Miembro).join(Libro).order_by(PrestamoInterno.fecha_prestamo.desc()).all()
        
        # Obtener préstamos externos activos
        prestamos_externos = PersonaPrestamo.query.filter(
            PersonaPrestamo.estado == 'activo'
        ).join(Libro).order_by(PersonaPrestamo.fecha_prestamo.desc()).all()
        
        # Obtener historial de préstamos internos
        historial_internos = PrestamoInterno.query.filter(
            PrestamoInterno.estado == 'devuelto'
        ).join(Miembro).join(Libro).order_by(PrestamoInterno.fecha_prestamo.desc()).all()
        
        # Obtener historial de préstamos externos
        historial_externos = PersonaPrestamo.query.filter(
            PersonaPrestamo.estado == 'devuelto'
        ).join(Libro).order_by(PersonaPrestamo.fecha_prestamo.desc()).all()
        
        # Verificar y corregir libros no disponibles sin préstamos activos
        libros_no_disponibles = Libro.query.filter_by(disponible=False).all()
        for libro in libros_no_disponibles:
            prestamo_activo_interno = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_activo_externo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            if not prestamo_activo_interno and not prestamo_activo_externo:
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
                             now=now,
                             timestamp=datetime.utcnow().timestamp())
    except Exception as e:
        print(f"Error en la ruta de gestión de préstamos: {str(e)}")
        flash('Error al cargar los préstamos', 'danger')
        return redirect(url_for('admin'))

@app.route('/admin/verificar-prestamos')
@admin_required
def verificar_prestamos():
    """Función para verificar y corregir inconsistencias en los préstamos"""
    try:
        cambios_realizados = []
        
        # Verificar libros marcados como no disponibles sin préstamos activos
        libros_no_disponibles = Libro.query.filter_by(disponible=False).all()
        for libro in libros_no_disponibles:
            prestamo_activo_interno = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_activo_externo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            
            if not prestamo_activo_interno and not prestamo_activo_externo:
                libro.disponible = True
                cambios_realizados.append(f"Libro '{libro.titulo}' marcado como disponible (no tenía préstamos activos)")
        
        # Verificar libros marcados como disponibles con préstamos activos
        libros_disponibles = Libro.query.filter_by(disponible=True).all()
        for libro in libros_disponibles:
            prestamo_activo_interno = PrestamoInterno.query.filter_by(libro_id=libro.id, estado='activo').first()
            prestamo_activo_externo = PersonaPrestamo.query.filter_by(libro_id=libro.id, estado='activo').first()
            
            if prestamo_activo_interno or prestamo_activo_externo:
                libro.disponible = False
                cambios_realizados.append(f"Libro '{libro.titulo}' marcado como no disponible (tenía préstamos activos)")
        
        if cambios_realizados:
            db.session.commit()
            flash(f'Se realizaron {len(cambios_realizados)} correcciones en la base de datos', 'info')
            for cambio in cambios_realizados:
                print(f"Corrección: {cambio}")
        else:
            flash('No se encontraron inconsistencias en los préstamos', 'success')
            
    except Exception as e:
        print(f"Error al verificar préstamos: {str(e)}")
        db.session.rollback()
        flash('Error al verificar los préstamos', 'danger')
    
    return redirect(url_for('admin_prestamos'))

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
        PrestamoInterno.query.filter(
            PrestamoInterno.estado == 'devuelto'
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

@app.route('/gestion_usuarios')
@superadmin_required
def gestion_usuarios():
    usuarios = Usuario.query.all()
    return render_template('gestion_usuarios.html', usuarios=usuarios)

@app.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@superadmin_required
def eliminar_usuario(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    if usuario.rol == 'superadmin':
        flash('No puedes eliminar al superadmin.', 'danger')
        return redirect(url_for('gestion_usuarios'))
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('gestion_usuarios'))

@app.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@superadmin_required
def editar_usuario(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    
    # No permitir editar superadmin
    if usuario.rol == 'superadmin':
        flash('No puedes editar al superadmin.', 'danger')
        return redirect(url_for('gestion_usuarios'))
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        usuario.username = request.form.get('username')
        usuario.nombre = request.form.get('nombre')
        usuario.apellido = request.form.get('apellido')
        usuario.email = request.form.get('email')
        usuario.telefono = request.form.get('telefono')
        usuario.cedula = request.form.get('cedula')
        usuario.rol = request.form.get('rol')
        usuario.is_admin = (usuario.rol in ['admin', 'superadmin'])
        
        # Si se proporcionó una nueva contraseña, actualizarla
        nueva_password = request.form.get('password')
        if nueva_password:
            usuario.set_password(nueva_password)
        
        try:
            db.session.commit()
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('gestion_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el usuario. Verifica que el nombre de usuario o email no estén en uso.', 'danger')
    
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/bienvenida')
def bienvenida():
    return render_template('bienvenida.html')

# ==================== RUTAS PARA GESTIÓN DE MIEMBROS ====================

@app.route('/miembros')
@admin_required
def miembros():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = request.args.get('q', '')
    estado = request.args.get('estado', '')
    
    # Construir la consulta base
    miembros_query = Miembro.query
    
    # Aplicar filtro de estado si se especifica
    if estado:
        miembros_query = miembros_query.filter(Miembro.estado == estado)
    
    # Aplicar búsqueda por texto si se especifica
    if query:
        search_term = f'%{query}%'
        miembros_query = miembros_query.filter(
            or_(
                Miembro.nombres.ilike(search_term),
                Miembro.apellidos.ilike(search_term),
                Miembro.cedula.ilike(search_term),
                Miembro.email.ilike(search_term),
                Miembro.numero_carnet.ilike(search_term)
            )
        )
    
    # Ordenar por apellidos
    miembros_query = miembros_query.order_by(Miembro.apellidos)
    
    # Paginar los resultados
    miembros = miembros_query.paginate(page=page, per_page=per_page)
    
    return render_template('admin/miembros.html', miembros=miembros, query=query, estado=estado)

@app.route('/miembros/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_miembro():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombres = request.form.get('nombres')
            apellidos = request.form.get('apellidos')
            cedula = request.form.get('cedula')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            direccion = request.form.get('direccion')
            
            # Validar campos requeridos
            if not all([nombres, apellidos, cedula, telefono, email, direccion]):
                flash('Todos los campos marcados con * son obligatorios', 'danger')
                return redirect(request.url)
            
            # Verificar si la cédula ya existe
            if Miembro.query.filter_by(cedula=cedula).first():
                flash('Ya existe un miembro con esta cédula', 'danger')
                return redirect(request.url)
            
            # Verificar si el email ya existe
            if Miembro.query.filter_by(email=email).first():
                flash('Ya existe un miembro con este correo electrónico', 'danger')
                return redirect(request.url)
            
            # Crear nuevo miembro
            miembro = Miembro(
                nombres=nombres,
                apellidos=apellidos,
                cedula=cedula,
                telefono=telefono,
                email=email,
                direccion=direccion,
                estado=request.form.get('estado', 'activo')
            )
            
            # Generar número de carnet
            miembro.numero_carnet = miembro.generar_numero_carnet()
            
            # Manejar la foto si se subió
            if 'foto' in request.files:
                foto = request.files['foto']
                if foto and foto.filename != '':
                    # Crear directorio para fotos si no existe
                    upload_folder = os.path.join(app.static_folder, 'uploads', 'fotos')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Generar nombre único para la foto
                    filename = f"miembro_{miembro.numero_carnet}_{foto.filename}"
                    foto_path = os.path.join(upload_folder, filename)
                    foto.save(foto_path)
                    miembro.foto = f"uploads/fotos/{filename}"
            
            db.session.add(miembro)
            db.session.commit()
            
            flash('Miembro registrado exitosamente', 'success')
            return redirect(url_for('miembros'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar miembro: {str(e)}")
            flash('Error al registrar el miembro', 'danger')
            return redirect(request.url)
    
    return render_template('admin/nuevo_miembro.html')

@app.route('/miembros/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_miembro(id):
    miembro = Miembro.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos
            miembro.nombres = request.form.get('nombres')
            miembro.apellidos = request.form.get('apellidos')
            miembro.telefono = request.form.get('telefono')
            miembro.email = request.form.get('email')
            miembro.direccion = request.form.get('direccion')
            miembro.estado = request.form.get('estado', 'activo')
            
            # Verificar cédula única (excluyendo el miembro actual)
            nueva_cedula = request.form.get('cedula')
            if nueva_cedula != miembro.cedula:
                if Miembro.query.filter_by(cedula=nueva_cedula).first():
                    flash('Ya existe un miembro con esta cédula', 'danger')
                    return redirect(request.url)
                miembro.cedula = nueva_cedula
            
            # Verificar email único (excluyendo el miembro actual)
            nuevo_email = request.form.get('email')
            if nuevo_email != miembro.email:
                if Miembro.query.filter_by(email=nuevo_email).first():
                    flash('Ya existe un miembro con este correo electrónico', 'danger')
                    return redirect(request.url)
            
            # Manejar nueva foto si se subió
            if 'foto' in request.files:
                foto = request.files['foto']
                if foto and foto.filename != '':
                    # Crear directorio para fotos si no existe
                    upload_folder = os.path.join(app.static_folder, 'uploads', 'fotos')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Eliminar foto anterior si existe
                    if miembro.foto:
                        foto_anterior = os.path.join(app.static_folder, miembro.foto)
                        if os.path.exists(foto_anterior):
                            os.remove(foto_anterior)
                    
                    # Guardar nueva foto
                    filename = f"miembro_{miembro.numero_carnet}_{foto.filename}"
                    foto_path = os.path.join(upload_folder, filename)
                    foto.save(foto_path)
                    miembro.foto = f"uploads/fotos/{filename}"
            
            db.session.commit()
            flash('Miembro actualizado exitosamente', 'success')
            return redirect(url_for('miembros'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar miembro: {str(e)}")
            flash('Error al actualizar el miembro', 'danger')
    
    return render_template('admin/editar_miembro.html', miembro=miembro)

@app.route('/miembros/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_miembro(id):
    miembro = Miembro.query.get_or_404(id)
    
    try:
        # Eliminar foto si existe
        if miembro.foto:
            foto_path = os.path.join(app.static_folder, miembro.foto)
            if os.path.exists(foto_path):
                os.remove(foto_path)
        
        db.session.delete(miembro)
        db.session.commit()
        flash('Miembro eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar miembro: {str(e)}")
        flash('Error al eliminar el miembro', 'danger')
    
    return redirect(url_for('miembros'))

@app.route('/miembros/<int:id>/carnet')
@admin_required
def ver_carnet(id):
    miembro = Miembro.query.get_or_404(id)
    return render_template('admin/carnet.html', miembro=miembro)

@app.route('/miembros/<int:id>/carnet/imprimir')
@admin_required
def imprimir_carnet(id):
    miembro = Miembro.query.get_or_404(id)
    return render_template('admin/carnet_imprimir.html', miembro=miembro)

@app.route('/api/miembros')
@admin_required
def api_miembros():
    search = request.args.get('search', '')
    miembros = Miembro.query.filter(
        or_(
            Miembro.nombres.ilike(f'%{search}%'),
            Miembro.apellidos.ilike(f'%{search}%'),
            Miembro.cedula.ilike(f'%{search}%'),
            Miembro.email.ilike(f'%{search}%'),
            Miembro.numero_carnet.ilike(f'%{search}%')
        )
    ).limit(10).all()
    
    return jsonify([{
        'id': miembro.id,
        'nombre_completo': miembro.nombre_completo,
        'cedula': miembro.cedula,
        'numero_carnet': miembro.numero_carnet,
        'estado': miembro.estado
    } for miembro in miembros])

# ==================== RUTAS PARA ESTADÍSTICAS ====================

@app.route('/estadisticas')
@admin_required
def estadisticas():
    """Vista principal de estadísticas"""
    try:
        # Estadísticas generales
        total_libros = Libro.query.count()
        libros_disponibles = Libro.query.filter_by(disponible=True).count()
        libros_prestados = Libro.query.filter_by(disponible=False).count()
        total_miembros = Miembro.query.count()
        miembros_activos = Miembro.query.filter_by(estado='activo').count()
        
        # Estadísticas de préstamos - CORREGIDO para incluir todos los tipos
        prestamos_activos = Prestamo.query.filter_by(estado='activo').count()
        prestamos_internos_activos = PrestamoInterno.query.filter_by(estado='activo').count()
        prestamos_externos_activos = PersonaPrestamo.query.filter_by(estado='activo').count()
        total_prestamos_activos = prestamos_activos + prestamos_internos_activos + prestamos_externos_activos
        
        # Préstamos devueltos - CORREGIDO para incluir todos los tipos
        prestamos_devueltos = Prestamo.query.filter_by(estado='devuelto').count()
        prestamos_internos_devueltos = PrestamoInterno.query.filter_by(estado='devuelto').count()
        prestamos_externos_devueltos = PersonaPrestamo.query.filter_by(estado='devuelto').count()
        total_prestamos_devueltos = prestamos_devueltos + prestamos_internos_devueltos + prestamos_externos_devueltos
        
        # Préstamos vencidos - CORREGIDO para incluir todos los tipos
        now = datetime.utcnow()
        prestamos_vencidos = Prestamo.query.filter(
            Prestamo.estado == 'activo',
            Prestamo.fecha_devolucion_esperada < now
        ).count()
        prestamos_internos_vencidos = PrestamoInterno.query.filter(
            PrestamoInterno.estado == 'activo',
            PrestamoInterno.fecha_devolucion_esperada < now
        ).count()
        prestamos_externos_vencidos = PersonaPrestamo.query.filter(
            PersonaPrestamo.estado == 'activo',
            PersonaPrestamo.fecha_devolucion_esperada < now
        ).count()
        total_prestamos_vencidos = prestamos_vencidos + prestamos_internos_vencidos + prestamos_externos_vencidos
        
        # Top 5 libros más prestados - CORREGIDO para incluir todos los tipos
        # Combinar préstamos de todos los tipos
        prestamos_todos = db.session.query(
            Libro.titulo,
            db.func.count(Prestamo.id).label('total_prestamos')
        ).join(Prestamo, Libro.id == Prestamo.libro_id).group_by(Libro.id)
        
        prestamos_internos_todos = db.session.query(
            Libro.titulo,
            db.func.count(PrestamoInterno.id).label('total_prestamos')
        ).join(PrestamoInterno, Libro.id == PrestamoInterno.libro_id).group_by(Libro.id)
        
        prestamos_externos_todos = db.session.query(
            Libro.titulo,
            db.func.count(PersonaPrestamo.id).label('total_prestamos')
        ).join(PersonaPrestamo, Libro.id == PersonaPrestamo.libro_id).group_by(Libro.id)
        
        # Combinar todos los resultados
        from collections import defaultdict
        libros_contador = defaultdict(int)
        
        for titulo, count in prestamos_todos.all():
            libros_contador[titulo] += count
        for titulo, count in prestamos_internos_todos.all():
            libros_contador[titulo] += count
        for titulo, count in prestamos_externos_todos.all():
            libros_contador[titulo] += count
        
        # Ordenar por total de préstamos y convertir a formato esperado por el template
        libros_mas_prestados = []
        for titulo, count in sorted(libros_contador.items(), key=lambda x: x[1], reverse=True)[:5]:
            # Crear un objeto con los atributos que espera el template
            libro_obj = type('Libro', (), {'titulo': titulo, 'total_prestamos': count})()
            libros_mas_prestados.append(libro_obj)
        
        # Top 5 miembros más activos - CORREGIDO para incluir PrestamoInterno
        miembros_mas_activos = db.session.query(
            Miembro.nombres,
            Miembro.apellidos,
            db.func.count(PrestamoInterno.id).label('total_prestamos')
        ).join(PrestamoInterno, Miembro.id == PrestamoInterno.miembro_id).group_by(Miembro.id).order_by(
            db.func.count(PrestamoInterno.id).desc()
        ).limit(5).all()
        
        # Imprimir información de depuración
        print(f"=== ESTADÍSTICAS DEBUG ===")
        print(f"Total libros: {total_libros}")
        print(f"Libros disponibles: {libros_disponibles}")
        print(f"Libros prestados: {libros_prestados}")
        print(f"Préstamos activos (Prestamo): {prestamos_activos}")
        print(f"Préstamos activos (PrestamoInterno): {prestamos_internos_activos}")
        print(f"Préstamos activos (PersonaPrestamo): {prestamos_externos_activos}")
        print(f"Total préstamos activos: {total_prestamos_activos}")
        print(f"Total préstamos devueltos: {total_prestamos_devueltos}")
        print(f"Total préstamos vencidos: {total_prestamos_vencidos}")
        
        return render_template('admin/estadisticas.html',
                             total_libros=total_libros,
                             libros_disponibles=libros_disponibles,
                             libros_prestados=libros_prestados,
                             total_miembros=total_miembros,
                             miembros_activos=miembros_activos,
                             total_prestamos_activos=total_prestamos_activos,
                             total_prestamos_devueltos=total_prestamos_devueltos,
                             total_prestamos_vencidos=total_prestamos_vencidos,
                             libros_mas_prestados=libros_mas_prestados,
                             miembros_mas_activos=miembros_mas_activos)
    except Exception as e:
        print(f"Error al cargar estadísticas: {str(e)}")
        flash('Error al cargar las estadísticas', 'danger')
        return redirect(url_for('admin'))

@app.route('/api/estadisticas/prestamos')
@admin_required
def api_estadisticas_prestamos():
    """API para obtener datos de préstamos por período"""
    periodo = request.args.get('periodo', 'mes')  # semana, mes, año
    
    try:
        now = datetime.utcnow()
        
        if periodo == 'semana':
            # Últimas 4 semanas
            fechas = []
            datos_internos = []
            datos_externos = []
            
            for i in range(4):
                fecha_inicio = now - timedelta(weeks=i+1)
                fecha_fin = now - timedelta(weeks=i)
                
                prestamos_internos = Prestamo.query.filter(
                    Prestamo.fecha_prestamo >= fecha_inicio,
                    Prestamo.fecha_prestamo < fecha_fin
                ).count()
                
                prestamos_externos = PersonaPrestamo.query.filter(
                    PersonaPrestamo.fecha_prestamo >= fecha_inicio,
                    PersonaPrestamo.fecha_prestamo < fecha_fin
                ).count()
                
                fechas.append(fecha_inicio.strftime('%d/%m'))
                datos_internos.append(prestamos_internos)
                datos_externos.append(prestamos_externos)
            
            fechas.reverse()
            datos_internos.reverse()
            datos_externos.reverse()
            
        elif periodo == 'mes':
            # Últimos 12 meses
            fechas = []
            datos_internos = []
            datos_externos = []
            
            for i in range(12):
                fecha_inicio = now.replace(day=1) - timedelta(days=30*i)
                fecha_fin = fecha_inicio.replace(day=1) + timedelta(days=30)
                
                prestamos_internos = Prestamo.query.filter(
                    Prestamo.fecha_prestamo >= fecha_inicio,
                    Prestamo.fecha_prestamo < fecha_fin
                ).count()
                
                prestamos_externos = PersonaPrestamo.query.filter(
                    PersonaPrestamo.fecha_prestamo >= fecha_inicio,
                    PersonaPrestamo.fecha_prestamo < fecha_fin
                ).count()
                
                fechas.append(fecha_inicio.strftime('%b %Y'))
                datos_internos.append(prestamos_internos)
                datos_externos.append(prestamos_externos)
            
            fechas.reverse()
            datos_internos.reverse()
            datos_externos.reverse()
            
        else:  # año
            # Últimos 5 años
            fechas = []
            datos_internos = []
            datos_externos = []
            
            for i in range(5):
                año = now.year - i
                fecha_inicio = datetime(año, 1, 1)
                fecha_fin = datetime(año + 1, 1, 1)
                
                prestamos_internos = Prestamo.query.filter(
                    Prestamo.fecha_prestamo >= fecha_inicio,
                    Prestamo.fecha_prestamo < fecha_fin
                ).count()
                
                prestamos_externos = PersonaPrestamo.query.filter(
                    PersonaPrestamo.fecha_prestamo >= fecha_inicio,
                    PersonaPrestamo.fecha_prestamo < fecha_fin
                ).count()
                
                fechas.append(str(año))
                datos_internos.append(prestamos_internos)
                datos_externos.append(prestamos_externos)
            
            fechas.reverse()
            datos_internos.reverse()
            datos_externos.reverse()
        
        return jsonify({
            'fechas': fechas,
            'prestamos_internos': datos_internos,
            'prestamos_externos': datos_externos,
            'periodo': periodo
        })
        
    except Exception as e:
        print(f"Error al obtener estadísticas de préstamos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas/categorias')
@admin_required
def api_estadisticas_categorias():
    """API para obtener estadísticas por categorías/materias"""
    try:
        # Obtener todas las materias únicas
        materias = db.session.query(Libro.materias).distinct().all()
        materias = [m[0] for m in materias if m[0] and m[0].strip()]
        
        datos_categorias = []
        for materia in materias[:10]:  # Top 10 categorías
            total_libros = Libro.query.filter(Libro.materias == materia).count()
            libros_prestados = db.session.query(Libro).join(Prestamo, Libro.id == Prestamo.libro_id).filter(
                Libro.materias == materia,
                Prestamo.estado == 'activo'
            ).count()
            
            datos_categorias.append({
                'materia': materia,
                'total_libros': total_libros,
                'libros_prestados': libros_prestados
            })
        
        # Ordenar por total de libros
        datos_categorias.sort(key=lambda x: x['total_libros'], reverse=True)
        
        return jsonify({
            'categorias': [d['materia'] for d in datos_categorias],
            'total_libros': [d['total_libros'] for d in datos_categorias],
            'libros_prestados': [d['libros_prestados'] for d in datos_categorias]
        })
        
    except Exception as e:
        print(f"Error al obtener estadísticas por categorías: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin/prestamo/<int:prestamo_id>/detalles')
@admin_required
def detalles_prestamo(prestamo_id):
    tipo = request.args.get('tipo', 'PrestamoInterno')
    
    try:
        if tipo == 'PrestamoInterno':
            prestamo = PrestamoInterno.query.get_or_404(prestamo_id)
            if not prestamo:
                flash('Préstamo no encontrado', 'danger')
                return redirect(url_for('admin_prestamos'))
            
            return render_template('admin/detalles_prestamo.html', 
                                 prestamo=prestamo, 
                                 tipo='interno',
                                 miembro=prestamo.miembro,
                                 libro=prestamo.libro)
        elif tipo == 'Prestamo':
            prestamo = Prestamo.query.get_or_404(prestamo_id)
            if not prestamo:
                flash('Préstamo no encontrado', 'danger')
                return redirect(url_for('admin_prestamos'))
            
            return render_template('admin/detalles_prestamo.html', 
                                 prestamo=prestamo, 
                                 tipo='usuario',
                                 usuario=prestamo.usuario,
                                 libro=prestamo.libro)
        else:  # PersonaPrestamo
            prestamo = PersonaPrestamo.query.get_or_404(prestamo_id)
            if not prestamo:
                flash('Préstamo no encontrado', 'danger')
                return redirect(url_for('admin_prestamos'))
            
            return render_template('admin/detalles_prestamo.html', 
                                 prestamo=prestamo, 
                                 tipo='externo',
                                 libro=prestamo.libro)
    except Exception as e:
        print(f"Error al obtener detalles del préstamo: {str(e)}")
        flash('Error al cargar los detalles del préstamo', 'danger')
        return redirect(url_for('admin_prestamos'))

@app.route('/admin/prestamo/devolver/interno/<int:prestamo_id>', methods=['POST'])
@admin_required
def devolver_libro_interno(prestamo_id):
    try:
        print(f"Intentando devolver préstamo interno ID: {prestamo_id}")
        prestamo = db.session.get(PrestamoInterno, prestamo_id)
        
        if not prestamo:
            print(f"Préstamo interno no encontrado: {prestamo_id}")
            flash('Préstamo no encontrado', 'danger')
            return redirect(url_for('admin_prestamos'))
        
        print(f"Estado actual del préstamo: {prestamo.estado}")
        print(f"Libro: {prestamo.libro.titulo}")
        print(f"Disponible antes: {prestamo.libro.disponible}")
            
        if prestamo.estado == 'activo':
            prestamo.marcar_como_devuelto()
            print(f"Estado después de marcar como devuelto: {prestamo.estado}")
            print(f"Disponible después: {prestamo.libro.disponible}")
            print(f"Fecha devolución real: {prestamo.fecha_devolucion_real}")
            
            db.session.commit()
            print("Cambios guardados en la base de datos")
            flash('Libro devuelto exitosamente', 'success')
        else:
            print(f"Préstamo ya no está activo, estado: {prestamo.estado}")
            flash('Este libro ya ha sido devuelto', 'warning')
            
    except Exception as e:
        print(f"Error al devolver libro interno: {str(e)}")
        db.session.rollback()
        flash('Error al devolver el libro', 'danger')
    
    # Forzar recarga de la página
    return redirect(url_for('admin_prestamos'))

@app.route('/seleccionar-tipo-prestamo-usuario/<int:libro_id>')
@login_required
def seleccionar_tipo_prestamo_usuario(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    
    if not libro.disponible:
        flash('Este libro no está disponible para préstamo', 'warning')
        return redirect(url_for('detalle_libro', id=libro.id))
    
    return render_template('seleccionar_tipo_prestamo_usuario.html', libro=libro)

@app.route('/fichas-multiples')
@admin_required
def fichas_multiples():
    """Vista para imprimir múltiples fichas bibliográficas en una página"""
    try:
        # Obtener todos los libros ordenados por título
        libros = Libro.query.order_by(Libro.titulo).all()
        
        return render_template('fichas_multiples.html', libros=libros)
    except Exception as e:
        print(f"Error al cargar fichas múltiples: {str(e)}")
        flash('Error al cargar las fichas', 'danger')
        return redirect(url_for('admin'))

def limpiar_nombre_archivo(nombre):
    """Limpia un nombre para que sea válido como nombre de archivo"""
    # Remover caracteres especiales que no son válidos en nombres de archivo
    nombre_limpio = re.sub(r'[<>:"/\\|?*]', '', nombre)
    # Reemplazar espacios y otros caracteres problemáticos
    nombre_limpio = re.sub(r'[()]', '', nombre_limpio)
    nombre_limpio = nombre_limpio.replace(' ', '_')
    # Limitar la longitud
    if len(nombre_limpio) > 100:
        nombre_limpio = nombre_limpio[:100]
    return nombre_limpio

if __name__ == '__main__':
    app.run(debug=True)