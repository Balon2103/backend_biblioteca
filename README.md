# Sistema Bibliotecario

Sistema de gestión de biblioteca desarrollado con Flask que permite administrar libros, préstamos y usuarios.

## Características

- Gestión de libros (agregar, editar, eliminar)
- Sistema de préstamos para usuarios internos y externos
- Historial de préstamos
- Visualización de detalles de usuarios
- Interfaz administrativa
- Búsqueda y filtrado de libros
- Gestión de préstamos vencidos

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/sistema-bibliotecario.git
cd sistema-bibliotecario
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Inicializar la base de datos:
```bash
python crear_admin.py
```

5. Ejecutar la aplicación:
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto

```
sistema_bibliotecario/
├── app/
│   ├── config/
│   │   └── config.py
│   │   
│   ├── models/
│   │   ├── libro.py
│   │   ├── prestamo.py
│   │   └── usuario.py
│   │   
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── prestamos.py
│   │   
│   ├── static/
│   │   
│   ├── templates/
│   │   
│   └── utils/
│   │   ├── decorators.py
│   │   └── helpers.py
│   │   
│   ├── instance/
│   │   
│   ├── venv/
│   │   
│   ├── .env
│   │   
│   ├── README.md
│   │   
│   └── requirements.txt
│   └── run.py
```

## Uso

1. Acceder a la aplicación con las credenciales de administrador:
   - Usuario: admin
   - Contraseña: admin123

2. Gestionar libros:
   - Agregar nuevos libros
   - Editar información de libros existentes
   - Eliminar libros

3. Gestionar préstamos:
   - Registrar préstamos a usuarios internos
   - Registrar préstamos a usuarios externos
   - Devolver libros
   - Ver historial de préstamos

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 