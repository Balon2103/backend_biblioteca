from flask import Blueprint, render_template, request
from app import db
from app.models.libro import Libro
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/libro/<int:id>')
def detalle_libro(id):
    libro = Libro.query.get_or_404(id)
    return render_template('detalle_libro.html', libro=libro)

@main.route('/libro/<int:id>/ficha')
def ficha_bibliografica(id):
    libro = Libro.query.get_or_404(id)
    return render_template('ficha_bibliografica.html', libro=libro) 