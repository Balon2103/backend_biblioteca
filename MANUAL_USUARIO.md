# 📚 MANUAL DE USUARIO - SISTEMA BIBLIOTECARIO FUPAGUA

## Índice
1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Recuperación de Contraseña](#recuperación-de-contraseña)
4. [Navegación Principal](#navegación-principal)
5. [Catálogo de Libros](#catálogo-de-libros)
6. [Sistema de Préstamos](#sistema-de-préstamos)
7. [Panel de Administración](#panel-de-administración)
8. [Gestión de Miembros](#gestión-de-miembros)
9. [Estadísticas](#estadísticas)
10. [Solución de Problemas](#solución-de-problemas)

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
- ✅ **Recuperación de contraseña** por correo electrónico
- ✅ **Acceso 24/7** al catálogo digital

---

## 2. Acceso al Sistema

### 2.1 Acceso Público
- **URL Local**: `http://localhost:5000`
- **URL Producción**: `https://bibliotecafupagua.onrender.com`
- **Funcionalidades disponibles**:
  - Ver página de bienvenida
  - Explorar catálogo de libros
  - Ver detalles de libros
  - Solicitar préstamos externos

### 2.2 Acceso Administrativo
- **URL**: `/login`
- **Credenciales por defecto**:
  - **Superadmin**: `superadmin` / `superadmin123`
  - **Admin**: `admin` / `admin123`

---

## 3. Recuperación de Contraseña

### 3.1 Proceso de Recuperación
Si olvidaste tu contraseña, puedes recuperarla siguiendo estos pasos:

1. **Acceder a la página de login**
2. **Hacer clic en "¿Olvidaste tu contraseña?"**
3. **Ingresar tu correo electrónico** registrado en el sistema
4. **Hacer clic en "Enviar instrucciones"**
5. **Revisar tu correo electrónico** (también revisar carpeta de spam)
6. **Hacer clic en el enlace** de recuperación en el correo
7. **Ingresar nueva contraseña** (dos veces para confirmar)
8. **Hacer clic en "Restablecer Contraseña"**

### 3.2 Información del Correo de Recuperación
El correo contiene:
- **Asunto**: "Recuperación de Contraseña - Sistema Bibliotecario"
- **Enlace seguro**: Para restablecer la contraseña
- **Vigencia**: El enlace expira en 1 hora por seguridad

### 3.3 Solución de Problemas
- **No recibes el correo**: Revisar carpeta de spam
- **Enlace expirado**: Solicitar nuevo correo de recuperación
- **Error al restablecer**: Verificar que las contraseñas coincidan

---

## 4. Navegación Principal

### 4.1 Barra de Navegación
```
🏠 Inicio | 📚 Catálogo | 👤 Mi Perfil | 🔧 Administración | 🚪 Cerrar Sesión
```

### 4.2 Menú de Administración (Solo para administradores)
```
📚 Gestión de Libros
👥 Gestión de Miembros  
📋 Gestión de Préstamos
📊 Estadísticas
```

---

## 5. Catálogo de Libros

### 5.1 Explorar el Catálogo
1. **Acceder**: Clic en "Catálogo" en la barra de navegación
2. **Vista**: Los libros se muestran en tarjetas con:
   - Portada del libro
   - Título y autor
   - Información básica
   - Estado de disponibilidad

### 5.2 Búsqueda y Filtros
- **Búsqueda por texto**: Busca en título, autor, editorial, COTA
- **Filtro por categoría**: Selecciona materias específicas
- **Paginación**: Navega entre páginas de resultados

### 5.3 Ver Detalles de un Libro
1. Clic en cualquier libro del catálogo
2. **Información disponible**:
   - Título, autor, editorial
   - COTA, año de edición, ciudad
   - Número de páginas, formato
   - Estado de disponibilidad
   - Opciones de préstamo

---

## 6. Sistema de Préstamos

### 6.1 Tipos de Préstamo

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

### 6.2 Gestión de Préstamos

#### Para Usuarios Regulares
- **Ver mis préstamos**: Acceder a "Mi Perfil" → "Mis Préstamos"
- **Devolver libros**: Clic en "Devolver" en cada préstamo activo

#### Para Administradores
- **Ver todos los préstamos**: Administración → Gestión de Préstamos
- **Devolver libros**: Clic en "Devolver" en cualquier préstamo
- **Ver historial**: Pestaña "Historial" en gestión de préstamos

---

## 7. Panel de Administración

### 7.1 Gestión de Libros

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

### 7.2 Gestión de Miembros

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

### 7.3 Gestión de Préstamos

#### Vista General
- **Préstamos Activos**: Lista de libros prestados actualmente
- **Historial**: Préstamos devueltos
- **Filtros**: Por tipo (interno/externo) y estado

#### Acciones Disponibles
- **Ver detalles**: Clic en cualquier préstamo
- **Devolver libro**: Clic en "Devolver"
- **Nuevo préstamo**: Clic en "Nuevo Préstamo"

---

## 8. Gestión de Miembros

### 8.1 Carnet Digital
- **Ver carnet**: Clic en "Ver Carnet" en cualquier miembro
- **Imprimir carnet**: Clic en "Imprimir Carnet"
- **Información incluida**:
  - Foto del miembro
  - Datos personales
  - Número de carnet único
  - Fecha de registro

### 8.2 Estados de Miembros
- **Activo**: Miembro con acceso completo
- **Inactivo**: Miembro suspendido temporalmente
- **Suspendido**: Miembro con restricciones

---

## 9. Estadísticas

### 9.1 Estadísticas Generales
- **Total de libros**: Cantidad total en el catálogo
- **Libros disponibles**: Libros no prestados
- **Libros prestados**: Libros actualmente en préstamo
- **Total de miembros**: Miembros registrados
- **Miembros activos**: Miembros con estado activo

### 9.2 Estadísticas de Préstamos
- **Préstamos activos**: Préstamos sin devolver
- **Préstamos devueltos**: Historial de préstamos
- **Préstamos vencidos**: Préstamos fuera de fecha
- **Libros más prestados**: Top 5 libros populares
- **Miembros más activos**: Top 5 miembros con más préstamos

### 9.3 Gráficos y Reportes
- **Gráfico de préstamos por período**: Semana, mes, año
- **Gráfico por categorías**: Préstamos por materia
- **Tendencias**: Evolución de préstamos en el tiempo

---

## 10. Solución de Problemas

### 10.1 Problemas de Acceso
- **Error 404**: Verificar URL correcta
- **Error de login**: Verificar credenciales
- **Sesión expirada**: Volver a iniciar sesión

### 10.2 Problemas de Préstamos
- **Libro no disponible**: Verificar estado en catálogo
- **Error al prestar**: Verificar datos del formulario
- **Error al devolver**: Contactar administrador

### 10.3 Problemas de Correo
- **No recibo correo de recuperación**: Revisar spam
- **Enlace expirado**: Solicitar nuevo correo
- **Error al restablecer**: Verificar contraseñas

### 10.4 Contacto de Soporte
- **Correo**: bibliotecajmd.fupagua@gmail.com
- **Horario**: En horario laboral
- **Respuesta**: 24-48 horas hábiles

---

## 11. Información Adicional

### 11.1 Acerca de la Biblioteca
La Biblioteca Juana Milano de Díaz es una biblioteca especializada que forma parte de la Fundación de Personas Autistas del Guárico (FUPAGUA). Lleva el nombre de Juana Josefa Milano Durán de Díaz, educadora y fundadora de la primera escuela en Puerto Ayacucho, Amazonas.

### 11.2 Horarios de Atención
- **Acceso al catálogo**: 24/7 (en línea)
- **Atención personalizada**: Horario laboral
- **Consultas por correo**: bibliotecajmd.fupagua@gmail.com

### 11.3 Políticas de Uso
- **Duración de préstamos**: 15 días por defecto
- **Renovación**: Consultar con administrador
- **Multas**: Por retraso en devoluciones
- **Responsabilidad**: Cuidado de libros prestados

---

**© 2025 Sistema Bibliotecario FUPAGUA - Todos los derechos reservados** 