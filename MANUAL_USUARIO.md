# 📚 MANUAL DE USUARIO - SISTEMA BIBLIOTECARIO FUPAGUA

## Índice
1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Navegación Principal](#navegación-principal)
4. [Catálogo de Libros](#catálogo-de-libros)
5. [Sistema de Préstamos](#sistema-de-préstamos)
6. [Panel de Administración](#panel-de-administración)
7. [Gestión de Miembros](#gestión-de-miembros)
8. [Estadísticas](#estadísticas)
9. [Solución de Problemas](#solución-de-problemas)

---

## 1. Introducción

El **Sistema Bibliotecario FUPAGUA** es una aplicación web desarrollada para gestionar la biblioteca especializada de la Fundación de Personas Autistas del Guárico. Este sistema permite administrar libros, préstamos, miembros y generar reportes estadísticos.

### Funcionalidades Principales:
- ✅ **Catálogo público** de libros con búsqueda y filtros
- ✅ **Sistema de préstamos** interno y externo
- ✅ **Gestión de miembros** con carnets digitales
- ✅ **Panel administrativo** completo
- ✅ **Estadísticas** en tiempo real
- ✅ **Gestión de portadas** de libros

---

## 2. Acceso al Sistema

### 2.1 Acceso Público
- **URL**: `http://localhost:5000`
- **Funcionalidades disponibles**:
  - Ver página de bienvenida
  - Explorar catálogo de libros
  - Ver detalles de libros
  - Solicitar préstamos externos

### 2.2 Acceso Administrativo
- **URL**: `http://localhost:5000/login`
- **Credenciales por defecto**:
  - **Superadmin**: `superadmin` / `superadmin123`
  - **Admin**: `admin` / `admin123`

---

## 3. Navegación Principal

### 3.1 Barra de Navegación
```
🏠 Inicio | 📚 Catálogo | 👤 Mi Perfil | 🔧 Administración | 🚪 Cerrar Sesión
```

### 3.2 Menú de Administración (Solo para administradores)
```
📚 Gestión de Libros
👥 Gestión de Miembros  
📋 Gestión de Préstamos
📊 Estadísticas
```

---

## 4. Catálogo de Libros

### 4.1 Explorar el Catálogo
1. **Acceder**: Clic en "Catálogo" en la barra de navegación
2. **Vista**: Los libros se muestran en tarjetas con:
   - Portada del libro
   - Título y autor
   - Información básica
   - Estado de disponibilidad

### 4.2 Búsqueda y Filtros
- **Búsqueda por texto**: Busca en título, autor, editorial, COTA
- **Filtro por categoría**: Selecciona materias específicas
- **Paginación**: Navega entre páginas de resultados

### 4.3 Ver Detalles de un Libro
1. Clic en cualquier libro del catálogo
2. **Información disponible**:
   - Título, autor, editorial
   - COTA, año de edición, ciudad
   - Número de páginas, formato
   - Estado de disponibilidad
   - Opciones de préstamo

---

## 5. Sistema de Préstamos

### 5.1 Tipos de Préstamo

#### Préstamo Interno (Miembros)
- **Requisitos**: Ser miembro registrado
- **Duración**: 15 días por defecto
- **Proceso**:
  1. Seleccionar libro disponible
  2. Elegir "Préstamo Interno"
  3. Seleccionar miembro
  4. Confirmar préstamo

#### Préstamo Externo (Visitantes)
- **Requisitos**: Llenar formulario de datos personales
- **Duración**: 15 días por defecto
- **Proceso**:
  1. Seleccionar libro disponible
  2. Elegir "Préstamo Externo"
  3. Completar formulario de datos
  4. Confirmar préstamo

### 5.2 Gestión de Préstamos

#### Para Usuarios Regulares
- **Ver mis préstamos**: Acceder a "Mi Perfil" → "Mis Préstamos"
- **Devolver libros**: Clic en "Devolver" en cada préstamo activo

#### Para Administradores
- **Ver todos los préstamos**: Administración → Gestión de Préstamos
- **Devolver libros**: Clic en "Devolver" en cualquier préstamo
- **Ver historial**: Pestaña "Historial" en gestión de préstamos

---

## 6. Panel de Administración

### 6.1 Gestión de Libros

#### Agregar Nuevo Libro
1. **Acceder**: Administración → Gestión de Libros → "Agregar Nuevo Libro"
2. **Completar formulario**:
   - **Información General**: Título, autor, COTA, editorial, año, ciudad, colección
   - **Detalles Físicos**: Medidas, páginas, formato, ejemplares, tomos, materias
   - **Portada**: Subir imagen (opcional)
3. **Guardar**: Clic en "Guardar Libro"

#### Editar Libro
1. **Acceder**: Clic en "Editar" en cualquier libro
2. **Modificar campos**: Cambiar información según necesidad
3. **Gestionar portada**:
   - **Subir nueva**: Seleccionar archivo
   - **Eliminar actual**: Marcar checkbox "Eliminar portada actual"
4. **Guardar cambios**: Clic en "Guardar Cambios"

#### Eliminar Libro
1. **Acceder**: Clic en "Eliminar" en cualquier libro
2. **Confirmar**: Clic en "Eliminar" en el diálogo de confirmación

### 6.2 Gestión de Miembros

#### Agregar Nuevo Miembro
1. **Acceder**: Administración → Gestión de Miembros → "Agregar Nuevo Miembro"
2. **Completar datos**:
   - Nombres y apellidos
   - Cédula (única)
   - Teléfono y email
   - Dirección
   - Foto (opcional)
3. **Guardar**: Clic en "Guardar Miembro"

#### Gestionar Miembros
- **Ver lista**: Administración → Gestión de Miembros
- **Editar**: Clic en "Editar" en cualquier miembro
- **Eliminar**: Clic en "Eliminar" (con confirmación)
- **Ver carnet**: Clic en "Ver Carnet" o "Imprimir Carnet"

### 6.3 Gestión de Préstamos

#### Vista General
- **Préstamos Activos**: Lista de libros prestados actualmente
- **Historial**: Préstamos devueltos
- **Filtros**: Por tipo (interno/externo) y estado

#### Acciones Disponibles
- **Ver detalles**: Clic en cualquier préstamo
- **Devolver libro**: Clic en "Devolver"
- **Nuevo préstamo**: Clic en "Nuevo Préstamo"

---

## 7. Gestión de Miembros

### 7.1 Carnet Digital
- **Ver carnet**: Clic en "Ver Carnet" en cualquier miembro
- **Imprimir carnet**: Clic en "Imprimir Carnet"
- **Información incluida**:
  - Foto del miembro
  - Datos personales
  - Número de carnet único
  - Fecha de registro

### 7.2 Estados de Miembros
- **Activo**: Miembro con acceso completo
- **Inactivo**: Miembro suspendido temporalmente
- **Suspendido**: Miembro con restricciones

---

## 8. Estadísticas

### 8.1 Acceso a Estadísticas
- **Ruta**: Administración → Estadísticas
- **Requisitos**: Permisos de administrador

### 8.2 Información Disponible
- **Resumen general**:
  - Total de libros
  - Total de miembros
  - Préstamos activos
  - Préstamos vencidos

- **Gráficos**:
  - Préstamos por período (mes/año)
  - Libros por categorías
  - Top libros más prestados

- **Reportes**:
  - Préstamos por tipo
  - Actividad reciente
  - Tendencias de uso

---

## 9. Solución de Problemas

### 9.1 Problemas Comunes

#### No puedo acceder al sistema
- **Verificar**: URL correcta (`http://localhost:5000`)
- **Verificar**: Servidor ejecutándose
- **Solución**: Reiniciar el servidor

#### Error al subir portada
- **Verificar**: Formato de imagen (JPG, PNG, GIF)
- **Verificar**: Tamaño máximo (5MB)
- **Verificar**: Caracteres especiales en título del libro

#### Libro no aparece como disponible
- **Verificar**: Si hay préstamos activos
- **Solución**: Revisar gestión de préstamos
- **Solución**: Marcar como devuelto si es necesario

#### Error de permisos
- **Verificar**: Tipo de usuario (admin/superadmin)
- **Verificar**: Sesión activa
- **Solución**: Cerrar sesión y volver a iniciar

### 9.2 Contacto de Soporte
- **Email**: bibliotecajmd.fupagua@gmail.com
- **Horario**: Horario laboral
- **Ubicación**: Ver ubicación en página de bienvenida

---

## 10. Consejos de Uso

### 10.1 Para Usuarios
- **Búsqueda eficiente**: Usa filtros por categoría
- **Préstamos responsables**: Devuelve libros a tiempo
- **Datos actualizados**: Mantén tu información de contacto actualizada

### 10.2 Para Administradores
- **Backup regular**: Respaldar base de datos periódicamente
- **Mantenimiento**: Revisar préstamos vencidos regularmente
- **Estadísticas**: Usar reportes para tomar decisiones informadas

---

**© 2025 Sistema Bibliotecario FUPAGUA - Todos los derechos reservados** 