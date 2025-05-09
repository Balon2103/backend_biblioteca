from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.libro import Libro
from app.models.usuario import Usuario
from app.utils.decorators import admin_required
from sqlalchemy import or_

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/libro/nuevo', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.index'))
    return render_template('admin/nuevo_libro.html')

@admin.route('/libro/<int:id>/editar', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.index'))
    return render_template('admin/editar_libro.html', libro=libro)

@admin.route('/libro/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado exitosamente', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/api/libros')
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