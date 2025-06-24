# Sistema de Gestión de Miembros - Biblioteca

## 📋 Descripción

El sistema de gestión de miembros permite administrar los usuarios registrados en la biblioteca, incluyendo la generación de carnets imprimibles con toda la información relevante.

## 🎯 Funcionalidades Implementadas

### ✅ Gestión Completa de Miembros
- **Registro de nuevos miembros** con todos los datos requeridos
- **Edición de información** de miembros existentes
- **Eliminación de miembros** con limpieza automática de archivos
- **Búsqueda y filtrado** por nombre, cédula, número de carnet
- **Filtrado por estado** (activo, inactivo, suspendido)
- **Paginación** para manejar grandes volúmenes de datos

### ✅ Datos del Miembro
- **Nombres y Apellidos** (campos separados)
- **Cédula de Identidad** (única, validación numérica)
- **Teléfono** (formato libre)
- **Dirección** (texto largo)
- **Foto del miembro** (opcional, con vista previa)
- **Número de carnet** (generado automáticamente)
- **Estado** (activo, inactivo, suspendido)
- **Fecha de registro** (automática)

### ✅ Sistema de Carnets
- **Vista previa del carnet** en pantalla
- **Carnet imprimible** optimizado para impresión
- **Diseño profesional** con información completa
- **Tamaño estándar** de carnet (85.6mm x 54mm)
- **Impresión automática** al abrir la vista de impresión

### ✅ Características Técnicas
- **Validación de datos** en frontend y backend
- **Manejo de archivos** con límites de tamaño (5MB)
- **Generación automática** de números de carnet únicos
- **API REST** para búsqueda de miembros
- **Interfaz responsiva** con Bootstrap 5
- **Iconografía** con Font Awesome

## 🚀 Instalación y Configuración

### 1. Migración de Base de Datos
```bash
python migrate_miembros.py
```

### 2. Crear Miembros de Ejemplo (Opcional)
```bash
python crear_miembros_ejemplo.py
```

### 3. Iniciar la Aplicación
```bash
python main.py
```

## 📱 Uso del Sistema

### Acceso a la Gestión de Miembros
1. Iniciar sesión como administrador
2. Ir al menú "Administración" → "Gestión de Miembros"

### Registrar un Nuevo Miembro
1. Hacer clic en "Nuevo Miembro"
2. Completar todos los campos obligatorios (*)
3. Opcionalmente subir una foto
4. Hacer clic en "Registrar Miembro"

### Ver/Imprimir Carnet
1. En la lista de miembros, hacer clic en el ícono de carnet (📋)
2. Para imprimir, hacer clic en "Imprimir Carnet" (🖨️)

### Editar Miembro
1. En la lista de miembros, hacer clic en el ícono de editar (✏️)
2. Modificar los campos necesarios
3. Hacer clic en "Actualizar Miembro"

## 🎨 Diseño del Carnet

### Información Incluida
- **Logo/Nombre de la Biblioteca**
- **Foto del miembro** (o placeholder)
- **Nombre completo**
- **Cédula de identidad**
- **Número de carnet** (destacado)
- **Teléfono**
- **Estado del miembro** (badge de color)
- **Fecha de registro**
- **Texto legal** ("Personal e intransferible")

### Características del Diseño
- **Tamaño estándar** de carnet de identificación
- **Diseño profesional** con gradientes y bordes
- **Tipografía clara** y legible
- **Colores institucionales** (azul y gris)
- **Optimizado para impresión** en blanco y negro

## 🔧 Estructura de Archivos

```
templates/admin/
├── miembros.html              # Vista principal de miembros
├── nuevo_miembro.html         # Formulario de registro
├── editar_miembro.html        # Formulario de edición
├── carnet.html               # Vista previa del carnet
└── carnet_imprimir.html      # Plantilla para impresión

static/uploads/fotos/          # Directorio para fotos de miembros

models.py                      # Modelo Miembro
main.py                        # Rutas y lógica de negocio
migrate_miembros.py           # Script de migración
crear_miembros_ejemplo.py     # Script de datos de ejemplo
```

## 📊 Base de Datos

### Tabla: miembros
```sql
CREATE TABLE miembros (
    id INTEGER PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    foto VARCHAR(255),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo',
    numero_carnet VARCHAR(20) UNIQUE
);
```

## 🔐 Seguridad y Validaciones

### Validaciones Frontend
- **Campos requeridos** marcados con asterisco
- **Validación de cédula** (solo números)
- **Validación de imagen** (tipo y tamaño)
- **Vista previa** de imagen antes de subir

### Validaciones Backend
- **Verificación de cédula única**
- **Validación de archivos** (tipo, tamaño)
- **Sanitización de datos** de entrada
- **Manejo de errores** con rollback

## 🎯 Rutas API

### Gestión de Miembros
- `GET /miembros` - Lista de miembros (con paginación y filtros)
- `GET /miembros/nuevo` - Formulario de nuevo miembro
- `POST /miembros/nuevo` - Crear nuevo miembro
- `GET /miembros/<id>/editar` - Formulario de edición
- `POST /miembros/<id>/editar` - Actualizar miembro
- `POST /miembros/<id>/eliminar` - Eliminar miembro

### Carnets
- `GET /miembros/<id>/carnet` - Ver carnet en pantalla
- `GET /miembros/<id>/carnet/imprimir` - Imprimir carnet

### API REST
- `GET /api/miembros?search=<texto>` - Búsqueda de miembros

## 🎨 Personalización

### Cambiar Colores del Carnet
Editar en `templates/admin/carnet_imprimir.html`:
```css
.carnet-header h3 {
    color: #007bff; /* Color principal */
}
```

### Cambiar Tamaño del Carnet
```css
.carnet-print {
    width: 85.6mm;  /* Ancho personalizable */
    height: 54mm;   /* Alto personalizable */
}
```

### Agregar Logo
Reemplazar el texto "BIBLIOTECA" con una imagen:
```html
<img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" style="height: 20px;">
```

## 🐛 Solución de Problemas

### Error: "No se puede crear el directorio de fotos"
```bash
mkdir -p static/uploads/fotos
```

### Error: "Tabla miembros no existe"
```bash
python migrate_miembros.py
```

### Error: "Permisos de escritura"
Verificar permisos en el directorio `static/uploads/fotos`

## 📈 Próximas Mejoras

- [ ] **Código QR** en el carnet con información del miembro
- [ ] **Renovación automática** de carnets vencidos
- [ ] **Importación masiva** desde archivos Excel/CSV
- [ ] **Exportación** de lista de miembros
- [ ] **Notificaciones** por email/SMS
- [ ] **Estadísticas** de membresía
- [ ] **Categorías** de miembros (estudiante, docente, etc.)

## 📞 Soporte

Para reportar problemas o solicitar mejoras, crear un issue en el repositorio del proyecto. 