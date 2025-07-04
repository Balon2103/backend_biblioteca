# 🔧 MANUAL TÉCNICO - SISTEMA BIBLIOTECARIO FUPAGUA

## Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Configuración de Correo Electrónico](#configuración-de-correo-electrónico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Base de Datos](#base-de-datos)
6. [API y Rutas](#api-y-rutas)
7. [Modelos de Datos](#modelos-de-datos)
8. [Autenticación y Autorización](#autenticación-y-autorización)
9. [Sistema de Recuperación de Contraseña](#sistema-de-recuperación-de-contraseña)
10. [Funcionalidades Principales](#funcionalidades-principales)
11. [Mantenimiento](#mantenimiento)
12. [Despliegue](#despliegue)
13. [Troubleshooting](#troubleshooting)

---

## 1. Arquitectura del Sistema

### 1.1 Tecnologías Utilizadas
- **Backend**: Flask (Python 3.8+)
- **Base de Datos**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Autenticación**: Session-based con Werkzeug
- **Correo Electrónico**: Flask-Mail con SMTP
- **Gráficos**: Chart.js para estadísticas
- **Tokens**: JWT para recuperación de contraseña

### 1.2 Patrón de Arquitectura
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Templates)   │◄──►│   (Flask App)   │◄──►│   (SQLite)      │
│   Bootstrap     │    │   Routes        │    │   SQLAlchemy    │
│   JavaScript    │    │   Models        │    │   ORM           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Email Service │
                       │   (SMTP/Gmail)  │
                       └─────────────────┘
```

### 1.3 Flujo de Datos
1. **Usuario** → **Frontend** (Templates)
2. **Frontend** → **Backend** (Routes/Controllers)
3. **Backend** → **Database** (Models/ORM)
4. **Backend** → **Email Service** (Recuperación de contraseña)
5. **Database** → **Backend** → **Frontend** → **Usuario**

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
Flask-Mail==0.9.1
Werkzeug==2.3.7
pandas==2.0.3
SQLAlchemy==2.0.21
PyJWT==2.8.0
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

#### Paso 5: Configurar Correo Electrónico
```bash
# Ejecutar script de configuración
python configurar_email.py
```

#### Paso 6: Ejecutar Aplicación
```bash
python main.py
```

### 2.3 Configuración de Variables de Entorno
```bash
# Crear archivo .env
SECRET_KEY=tu_clave_secreta_aqui
FLASK_ENV=development
DATABASE_URL=sqlite:///biblioteca.db

# Configuración de correo electrónico
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
MAIL_DEFAULT_SENDER=tu_correo@gmail.com

# Configuración del servidor
SERVER_NAME=localhost:5000
PREFERRED_URL_SCHEME=http
```

---

## 3. Configuración de Correo Electrónico

### 3.1 Configuración de Gmail

#### Paso 1: Activar Verificación en Dos Pasos
1. Ir a [myaccount.google.com](https://myaccount.google.com)
2. Seguridad → Verificación en dos pasos
3. Activar verificación en dos pasos

#### Paso 2: Generar Contraseña de Aplicación
1. Seguridad → Contraseñas de aplicación
2. Seleccionar "Correo" y "Windows"
3. Generar contraseña de 16 caracteres
4. Copiar la contraseña generada

#### Paso 3: Configurar Variables de Entorno
```bash
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=contraseña_de_aplicacion_generada
MAIL_DEFAULT_SENDER=tu_correo@gmail.com
```

### 3.2 Script de Configuración Automática
```bash
# Ejecutar script interactivo
python configurar_email.py
```

El script guía al usuario para:
- Ingresar correo Gmail
- Ingresar contraseña de aplicación
- Crear archivo .env automáticamente
- Probar envío de correo

### 3.3 Configuración para Producción (Render)
```bash
# Variables de entorno en Render
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=contraseña_de_aplicacion
MAIL_DEFAULT_SENDER=tu_correo@gmail.com
SERVER_NAME=bibliotecafupagua.onrender.com
PREFERRED_URL_SCHEME=https
```

---

## 4. Estructura del Proyecto

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
│   ├── 📁 emails/                   # Plantillas de correo
│   │   ├── password_reset.html
│   │   ├── password_reset.txt
│   │   ├── welcome.html
│   │   └── welcome.txt
│   └── base.html
├── 📁 utils/                        # Utilidades
│   └── email_service.py            # Servicio de correo
├── 📁 data/                         # Datos de ejemplo
│   └── libros.xlsx
├── 📄 main.py                       # Aplicación principal
├── 📄 models.py                     # Modelos de datos
├── 📄 extensions.py                 # Extensiones Flask
├── 📄 requirements.txt              # Dependencias
├── 📄 biblioteca.db                 # Base de datos SQLite
├── 📄 configurar_email.py          # Script de configuración
├── 📄 .env                          # Variables de entorno
└── 📄 README.md                     # Documentación
```

---

## 5. Base de Datos

### 5.1 Esquema de Base de Datos

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
    telefono VARCHAR(20),
    reset_token VARCHAR(255),
    reset_token_expiry DATETIME
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
    portada VARCHAR(255),
    disponible BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: `miembros`
```sql
CREATE TABLE miembros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    email VARCHAR(120),
    direccion TEXT,
    foto VARCHAR(255),
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: `prestamos`
```sql
CREATE TABLE prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id INTEGER,
    tipo_prestamo VARCHAR(20),
    nombre_prestatario VARCHAR(100),
    cedula_prestatario VARCHAR(20),
    telefono_prestatario VARCHAR(20),
    email_prestatario VARCHAR(120),
    direccion_prestatario TEXT,
    miembro_id INTEGER,
    fecha_prestamo DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion_esperada DATETIME,
    fecha_devolucion_real DATETIME,
    estado VARCHAR(20) DEFAULT 'activo',
    observaciones TEXT,
    FOREIGN KEY (libro_id) REFERENCES libros (id),
    FOREIGN KEY (miembro_id) REFERENCES miembros (id)
);
```

### 5.2 Relaciones
- **usuarios** ↔ **prestamos** (1:N)
- **libros** ↔ **prestamos** (1:N)
- **libros** ↔ **personas_prestamo** (1:N)
- **miembros** ↔ **prestamos_internos** (1:N)

---

## 6. API y Rutas

### 6.1 Rutas de Autenticación
```python
# Rutas principales
@app.route('/login', methods=['GET', 'POST'])
@app.route('/logout')
@app.route('/registro', methods=['GET', 'POST'])

# Recuperación de contraseña
@app.route('/recuperar-contrasena', methods=['GET', 'POST'])
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
```

### 6.2 Rutas de Administración
```python
# Gestión de libros
@app.route('/admin/libros')
@app.route('/admin/libros/nuevo', methods=['GET', 'POST'])
@app.route('/admin/libros/editar/<int:id>', methods=['GET', 'POST'])
@app.route('/admin/libros/eliminar/<int:id>')

# Gestión de miembros
@app.route('/admin/miembros')
@app.route('/admin/miembros/nuevo', methods=['GET', 'POST'])
@app.route('/admin/miembros/editar/<int:id>', methods=['GET', 'POST'])
@app.route('/admin/miembros/eliminar/<int:id>')

# Gestión de préstamos
@app.route('/admin/prestamos')
@app.route('/admin/prestamos/nuevo', methods=['GET', 'POST'])
@app.route('/admin/prestamos/devolver/<int:id>')

# Estadísticas
@app.route('/admin/estadisticas')
```

### 6.3 Rutas Públicas
```python
# Catálogo y bienvenida
@app.route('/')
@app.route('/catalogo')
@app.route('/libro/<int:id>')

# Préstamos externos
@app.route('/prestar-libro/<int:id>', methods=['GET', 'POST'])
@app.route('/nuevo-prestamo-externo', methods=['GET', 'POST'])
```

---

## 7. Modelos de Datos

### 7.1 Modelo Usuario
```python
class Usuario(db.Model):
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
    reset_token = db.Column(db.String(255))
    reset_token_expiry = db.Column(db.DateTime)
```

### 7.2 Modelo Libro
```python
class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    autor = db.Column(db.String(200))
    cota = db.Column(db.String(50))
    verificacion = db.Column(db.String(50))
    anio_edicion = db.Column(db.String(20))
    medidas = db.Column(db.String(50))
    num_paginas = db.Column(db.String(20))
    ciudad = db.Column(db.String(100))
    editorial = db.Column(db.String(200))
    coleccion = db.Column(db.String(200))
    materias = db.Column(db.Text)
    caract_formato = db.Column(db.String(100))
    cant_ejemplares = db.Column(db.String(20))
    tomos = db.Column(db.String(50))
    portada = db.Column(db.String(255))
    disponible = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 8. Autenticación y Autorización

### 8.1 Sistema de Login
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('admin_dashboard'))
    
    return render_template('login.html')
```

### 8.2 Decoradores de Autorización
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

---

## 9. Sistema de Recuperación de Contraseña

### 9.1 Generación de Tokens
```python
def generate_reset_token(user_id):
    """Genera un token seguro para recuperación de contraseña"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Expira en 1 hora
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_reset_token(token):
    """Verifica y decodifica el token de recuperación"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### 9.2 Envío de Correo de Recuperación
```python
def send_password_reset_email(user):
    """Envía correo de recuperación de contraseña"""
    token = generate_reset_token(user.id)
    
    # Guardar token en base de datos
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()
    
    # Enviar correo
    reset_url = url_for('reset_password', token=token, _external=True)
    
    msg = Message(
        'Recuperación de Contraseña - Sistema Bibliotecario',
        recipients=[user.email],
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    
    msg.html = render_template('emails/password_reset.html', 
                             user=user, reset_url=reset_url)
    msg.body = render_template('emails/password_reset.txt', 
                             user=user, reset_url=reset_url)
    
    mail.send(msg)
```

### 9.3 Rutas de Recuperación
```python
@app.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        user = Usuario.query.filter_by(email=email).first()
        
        if user:
            send_password_reset_email(user)
            flash('Se han enviado las instrucciones a tu correo electrónico.', 'success')
        else:
            flash('No se encontró una cuenta con ese correo electrónico.', 'error')
        
        return redirect(url_for('login'))
    
    return render_template('recuperar_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash('El enlace de recuperación es inválido o ha expirado.', 'error')
        return redirect(url_for('login'))
    
    user = Usuario.query.get(user_id)
    if not user:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
        else:
            user.password_hash = generate_password_hash(password)
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            flash('Tu contraseña ha sido actualizada exitosamente.', 'success')
            return redirect(url_for('login'))
    
    return render_template('reset_password.html')
```

---

## 10. Funcionalidades Principales

### 10.1 Gestión de Libros
- **CRUD completo**: Crear, leer, actualizar, eliminar
- **Subida de portadas**: Gestión de imágenes
- **Búsqueda y filtros**: Por título, autor, categoría
- **Estado de disponibilidad**: Control automático

### 10.2 Gestión de Miembros
- **Registro de miembros**: Con foto y datos completos
- **Carnets digitales**: Generación e impresión
- **Estados de miembros**: Activo, inactivo, suspendido
- **Historial de préstamos**: Por miembro

### 10.3 Sistema de Préstamos
- **Préstamos internos**: Para miembros registrados
- **Préstamos externos**: Para visitantes
- **Control de fechas**: Devolución automática
- **Estados de préstamos**: Activo, devuelto, vencido

### 10.4 Estadísticas y Reportes
- **Dashboard administrativo**: Resumen general
- **Gráficos interactivos**: Chart.js
- **Reportes detallados**: Por período, categoría, miembro
- **Exportación de datos**: CSV, Excel

---

## 11. Mantenimiento

### 11.1 Backup de Base de Datos
```bash
# Backup manual
cp biblioteca.db backup/biblioteca_$(date +%Y%m%d_%H%M%S).db

# Script de backup automático
python backup_database.py
```

### 11.2 Limpieza de Archivos
```bash
# Limpiar archivos temporales
rm -rf static/uploads/temp/*

# Limpiar logs antiguos
find logs/ -name "*.log" -mtime +30 -delete
```

### 11.3 Actualización de Dependencias
```bash
# Actualizar requirements.txt
pip freeze > requirements.txt

# Actualizar en producción
pip install -r requirements.txt --upgrade
```

---

## 12. Despliegue

### 12.1 Despliegue Local
```bash
# Configurar variables de entorno
cp .env.example .env
# Editar .env con configuración local

# Ejecutar aplicación
python main.py
```

### 12.2 Despliegue en Render

#### Configuración del Repositorio
1. **Conectar GitHub**: Vincular repositorio en Render
2. **Configurar build**: Python 3.8+
3. **Comando de build**: `pip install -r requirements.txt`
4. **Comando de start**: `python main.py`

#### Variables de Entorno en Render
```bash
SECRET_KEY=tu_clave_secreta_muy_segura
FLASK_ENV=production
DATABASE_URL=sqlite:///biblioteca.db

# Configuración de correo
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=contraseña_de_aplicacion
MAIL_DEFAULT_SENDER=tu_correo@gmail.com

# Configuración del servidor
SERVER_NAME=bibliotecafupagua.onrender.com
PREFERRED_URL_SCHEME=https
```

#### Configuración de Dominio
- **URL personalizada**: Configurar en Render
- **SSL automático**: Render proporciona certificado
- **Redirección HTTPS**: Automática

### 12.3 Scripts de Despliegue
```bash
# Script para configurar variables en Render
python configurar_render_email.py
```

---

## 13. Troubleshooting

### 13.1 Problemas de Correo Electrónico

#### Error: "SMTP Authentication failed"
```bash
# Solución: Verificar contraseña de aplicación
1. Ir a myaccount.google.com
2. Seguridad → Contraseñas de aplicación
3. Generar nueva contraseña
4. Actualizar MAIL_PASSWORD en .env
```

#### Error: "Connection refused"
```bash
# Solución: Verificar configuración SMTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

#### Error: "UnicodeEncodeError"
```bash
# Solución: Configurar codificación UTF-8
# En main.py, agregar:
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
```

### 13.2 Problemas de Base de Datos

#### Error: "Database is locked"
```bash
# Solución: Verificar permisos y conexiones
1. Cerrar todas las conexiones a la base de datos
2. Verificar permisos de escritura
3. Reiniciar aplicación
```

#### Error: "Table already exists"
```bash
# Solución: Eliminar base de datos y recrear
rm biblioteca.db
python crear_admin.py
```

### 13.3 Problemas de Despliegue

#### Error 404 en Render
```bash
# Solución: Verificar SERVER_NAME
SERVER_NAME=bibliotecafupagua.onrender.com
PREFERRED_URL_SCHEME=https
```

#### Error de importación
```bash
# Solución: Verificar requirements.txt
# Asegurar que todas las dependencias estén listadas
pip freeze > requirements.txt
```

### 13.4 Logs y Debugging
```python
# Configurar logging detallado
import logging
logging.basicConfig(level=logging.DEBUG)

# En funciones críticas
app.logger.debug('Mensaje de debug')
app.logger.error('Mensaje de error')
```

---

## 14. Seguridad

### 14.1 Mejores Prácticas
- **Contraseñas seguras**: Hash con Werkzeug
- **Tokens JWT**: Para recuperación de contraseña
- **Validación de entrada**: Sanitización de datos
- **CSRF Protection**: Tokens en formularios
- **Rate Limiting**: Límite de intentos de login

### 14.2 Configuración de Seguridad
```python
# Configuraciones de seguridad
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True  # Solo HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
```

---

**© 2025 Sistema Bibliotecario FUPAGUA - Documentación Técnica** 