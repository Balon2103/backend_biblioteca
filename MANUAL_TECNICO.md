# 🔧 MANUAL TÉCNICO - SISTEMA BIBLIOTECARIO FUPAGUA

## Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Base de Datos](#base-de-datos)
5. [API y Rutas](#api-y-rutas)
6. [Modelos de Datos](#modelos-de-datos)
7. [Autenticación y Autorización](#autenticación-y-autorización)
8. [Funcionalidades Principales](#funcionalidades-principales)
9. [Mantenimiento](#mantenimiento)
10. [Despliegue](#despliegue)
11. [Troubleshooting](#troubleshooting)

---

## 1. Arquitectura del Sistema

### 1.1 Tecnologías Utilizadas
- **Backend**: Flask (Python 3.8+)
- **Base de Datos**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Autenticación**: Session-based con Werkzeug
- **Gráficos**: Chart.js para estadísticas

### 1.2 Patrón de Arquitectura
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Templates)   │◄──►│   (Flask App)   │◄──►│   (SQLite)      │
│   Bootstrap     │    │   Routes        │    │   SQLAlchemy    │
│   JavaScript    │    │   Models        │    │   ORM           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.3 Flujo de Datos
1. **Usuario** → **Frontend** (Templates)
2. **Frontend** → **Backend** (Routes/Controllers)
3. **Backend** → **Database** (Models/ORM)
4. **Database** → **Backend** → **Frontend** → **Usuario**

---

## 2. Instalación y Configuración

### 2.1 Requisitos del Sistema
```bash
# Sistema Operativo
- Windows 10/11, Linux, macOS
- Python 3.8 o superior
- 4GB RAM mínimo
- 1GB espacio en disco

# Dependencias Python
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
Werkzeug==2.3.7
pandas==2.0.3
SQLAlchemy==2.0.21
```

### 2.2 Instalación Paso a Paso

#### Paso 1: Clonar Repositorio
```bash
git clone <repository-url>
cd Sistema_bibliotecario
```

#### Paso 2: Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar Base de Datos
```bash
# Crear usuarios administradores
python crear_admin.py

# O ejecutar directamente
python main.py
```

#### Paso 5: Ejecutar Aplicación
```bash
python main.py
```

### 2.3 Configuración de Variables de Entorno
```bash
# Crear archivo .env
SECRET_KEY=tu_clave_secreta_aqui
FLASK_ENV=development
DATABASE_URL=sqlite:///biblioteca.db
```

---

## 3. Estructura del Proyecto

```
Sistema_bibliotecario/
├── 📁 app/                          # Estructura modular (opcional)
│   ├── 📁 config/
│   │   └── config.py
│   ├── 📁 controllers/
│   │   └── books_controller.rb
│   ├── 📁 models/
│   │   ├── book.rb
│   │   ├── libro.py
│   │   ├── prestamo.py
│   │   └── usuario.py
│   ├── 📁 routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── prestamos.py
│   ├── 📁 templates/
│   │   └── admin/
│   │       └── index.html
│   └── 📁 utils/
│       ├── decorators.py
│       ├── google_books.py
│       └── helpers.py
├── 📁 static/                       # Archivos estáticos
│   ├── 📁 css/
│   │   └── style.css
│   ├── 📁 js/
│   │   ├── main.js
│   │   └── pagination.js
│   └── 📁 uploads/                  # Archivos subidos
│       ├── 📁 biografia/
│       ├── 📁 fotos/
│       └── 📁 portadas/
├── 📁 templates/                    # Plantillas principales
│   ├── 📁 admin/
│   ├── 📁 auth/
│   └── base.html
├── 📁 data/                         # Datos de ejemplo
│   └── libros.xlsx
├── 📄 main.py                       # Aplicación principal
├── 📄 models.py                     # Modelos de datos
├── 📄 extensions.py                 # Extensiones Flask
├── 📄 requirements.txt              # Dependencias
├── 📄 biblioteca.db                 # Base de datos SQLite
└── 📄 README.md                     # Documentación
```

---

## 4. Base de Datos

### 4.1 Esquema de Base de Datos

#### Tabla: `usuarios`
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    is_admin BOOLEAN DEFAULT FALSE,
    rol VARCHAR(20) DEFAULT 'usuario',
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    email VARCHAR(120) UNIQUE,
    telefono VARCHAR(20)
);
```

#### Tabla: `libros`
```sql
CREATE TABLE libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200),
    autor VARCHAR(200),
    cota VARCHAR(50),
    verificacion VARCHAR(50),
    anio_edicion VARCHAR(20),
    medidas VARCHAR(50),
    num_paginas VARCHAR(20),
    ciudad VARCHAR(100),
    editorial VARCHAR(200),
    coleccion VARCHAR(200),
    materias TEXT,
    caract_formato VARCHAR(100),
    cant_ejemplares VARCHAR(20),
    tomos VARCHAR(50),
    disponible BOOLEAN DEFAULT TRUE,
    portada VARCHAR(255)
);
```

#### Tabla: `prestamos`
```sql
CREATE TABLE prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    fecha_prestamo DATETIME NOT NULL,
    fecha_devolucion_esperada DATETIME NOT NULL,
    fecha_devolucion_real DATETIME,
    estado VARCHAR(20) DEFAULT 'activo',
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (libro_id) REFERENCES libros (id)
);
```

#### Tabla: `miembros`
```sql
CREATE TABLE miembros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    foto VARCHAR(255),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo',
    numero_carnet VARCHAR(20) UNIQUE
);
```

### 4.2 Relaciones
- **usuarios** ↔ **prestamos** (1:N)
- **libros** ↔ **prestamos** (1:N)
- **libros** ↔ **personas_prestamo** (1:N)
- **miembros** ↔ **prestamos_internos** (1:N)

---

## 5. API y Rutas

### 5.1 Rutas Principales

#### Rutas Públicas
```python
@app.route('/')                    # Página de bienvenida
@app.route('/catalogo')            # Catálogo de libros
@app.route('/libro/<int:id>')      # Detalle de libro
@app.route('/login')               # Inicio de sesión
@app.route('/registro')            # Registro de usuarios
```

#### Rutas de Administración
```python
@app.route('/admin')               # Panel principal
@app.route('/admin/libro/nuevo')   # Agregar libro
@app.route('/admin/libro/<int:id>/editar')  # Editar libro
@app.route('/admin/libro/<int:id>/eliminar') # Eliminar libro
@app.route('/miembros')            # Gestión de miembros
@app.route('/admin/prestamos')     # Gestión de préstamos
@app.route('/estadisticas')        # Estadísticas
```

#### Rutas de Préstamos
```python
@app.route('/prestamo/nuevo/<int:libro_id>')      # Préstamo interno
@app.route('/prestamo/externo/<int:libro_id>')    # Préstamo externo
@app.route('/prestamo/interno/<int:libro_id>')    # Préstamo interno (admin)
@app.route('/prestamo/devolver/<int:prestamo_id>') # Devolver libro
```

### 5.2 APIs JSON
```python
@app.route('/api/libros')          # Lista de libros
@app.route('/api/miembros')        # Lista de miembros
@app.route('/api/prestamo/<int:prestamo_id>')  # Detalles de préstamo
@app.route('/api/estadisticas/prestamos')      # Estadísticas de préstamos
@app.route('/api/estadisticas/categorias')     # Estadísticas por categorías
```

---

## 6. Modelos de Datos

### 6.1 Modelo Usuario
```python
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    rol = db.Column(db.String(20), default='usuario')
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    cedula = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.String(20))
    
    # Métodos
    def set_password(self, password)
    def check_password(self, password)
    def get_reset_token(self)
    @property
    def is_superadmin(self)
```

### 6.2 Modelo Libro
```python
class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    autor = db.Column(db.String(200))
    cota = db.Column(db.String(50))
    editorial = db.Column(db.String(200))
    anio_edicion = db.Column(db.String(20))
    ciudad = db.Column(db.String(100))
    coleccion = db.Column(db.String(200))
    materias = db.Column(db.Text)
    disponible = db.Column(db.Boolean, default=True)
    portada = db.Column(db.String(255))
    
    # Relaciones
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)
```

### 6.3 Modelo Préstamo
```python
class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'))
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')
```

---

## 7. Autenticación y Autorización

### 7.1 Decoradores de Autorización
```python
def login_required(f):
    """Requiere que el usuario esté autenticado"""
    
def admin_required(f):
    """Requiere permisos de administrador"""
    
def superadmin_required(f):
    """Requiere permisos de superadministrador"""
```

### 7.2 Niveles de Usuario
- **Usuario Regular**: Acceso al catálogo y préstamos personales
- **Admin**: Gestión completa de libros, préstamos y miembros
- **Superadmin**: Gestión de usuarios y configuración del sistema

### 7.3 Gestión de Sesiones
```python
# Iniciar sesión
session['user_id'] = user.id
session['is_admin'] = user.is_admin
session['rol'] = user.rol

# Verificar sesión
if 'user_id' in session:
    user = Usuario.query.get(session['user_id'])
```

---

## 8. Funcionalidades Principales

### 8.1 Gestión de Libros
- **CRUD completo**: Crear, Leer, Actualizar, Eliminar
- **Búsqueda avanzada**: Por título, autor, editorial, COTA
- **Filtros por categoría**: Basado en el campo `materias`
- **Gestión de portadas**: Subir, actualizar, eliminar imágenes
- **Paginación**: 12 libros por página en catálogo, 20 en admin

### 8.2 Sistema de Préstamos
- **Dos tipos**: Interno (miembros) y Externo (visitantes)
- **Control de disponibilidad**: Automático
- **Fechas de devolución**: 15 días por defecto
- **Estados**: Activo, Devuelto, Vencido
- **Historial completo**: Seguimiento de todos los préstamos

### 8.3 Gestión de Miembros
- **Registro completo**: Datos personales y de contacto
- **Carnets digitales**: Generación automática con foto
- **Estados**: Activo, Inactivo, Suspendido
- **Números únicos**: Generación automática de carnets

### 8.4 Estadísticas
- **Dashboard en tiempo real**: Totales y métricas
- **Gráficos interactivos**: Chart.js
- **Reportes por período**: Mensual y anual
- **Top libros**: Más prestados por categoría

---

## 9. Mantenimiento

### 9.1 Backup de Base de Datos
```bash
# Backup manual
cp biblioteca.db backup_biblioteca_$(date +%Y%m%d).db

# Script de backup automático
python backup_db.py
```

### 9.2 Limpieza de Archivos
```bash
# Limpiar archivos de portadas no utilizadas
python limpiar_portadas_huérfanas.py

# Verificar integridad de base de datos
python verificar_db.py
```

### 9.3 Logs y Monitoreo
```python
# Configurar logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('biblioteca.log'),
        logging.StreamHandler()
    ]
)
```

### 9.4 Actualizaciones
```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Migrar base de datos
python migrate_db.py

# Verificar integridad
python verificar_db.py
```

---

## 10. Despliegue

### 10.1 Configuración de Producción
```python
# config.py
class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 10.2 Servidor WSGI
```python
# wsgi.py
from main import app

if __name__ == "__main__":
    app.run()
```

### 10.3 Variables de Entorno
```bash
# .env
FLASK_ENV=production
SECRET_KEY=clave_super_secreta_produccion
DATABASE_URL=sqlite:///biblioteca_prod.db
```

### 10.4 Despliegue con Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

---

## 11. Troubleshooting

### 11.1 Errores Comunes

#### Error: "No module named 'flask'"
```bash
# Solución: Activar entorno virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

#### Error: "Database is locked"
```bash
# Solución: Verificar procesos
# Reiniciar aplicación
# Verificar permisos de archivo
```

#### Error: "Port already in use"
```bash
# Solución: Cambiar puerto
python main.py --port 5001

# O matar proceso
lsof -ti:5000 | xargs kill -9
```

### 11.2 Debugging
```python
# Habilitar debug mode
app.run(debug=True)

# Logging detallado
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### 11.3 Performance
```python
# Optimizar consultas
libros = Libro.query.options(
    db.joinedload(Libro.prestamos)
).all()

# Índices de base de datos
CREATE INDEX idx_libros_titulo ON libros(titulo);
CREATE INDEX idx_prestamos_fecha ON prestamos(fecha_prestamo);
```

---

## 12. Desarrollo

### 12.1 Estructura para Nuevas Funcionalidades
```python
# 1. Crear modelo en models.py
# 2. Crear rutas en main.py
# 3. Crear templates en templates/
# 4. Crear estilos en static/css/
# 5. Crear JavaScript en static/js/
# 6. Actualizar documentación
```

### 12.2 Convenciones de Código
- **PEP 8**: Estilo de código Python
- **Nombres descriptivos**: Variables y funciones claras
- **Documentación**: Docstrings en funciones principales
- **Comentarios**: Explicar lógica compleja

### 12.3 Testing
```python
# Ejemplo de test básico
import unittest
from main import app

class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
```

---

**© 2025 Sistema Bibliotecario FUPAGUA - Documentación Técnica** 