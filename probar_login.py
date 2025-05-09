from app import db
from app.models.usuario import Usuario

def probar_login(username, password):
    user = Usuario.query.filter_by(username=username).first()
    if user:
        print(f"Usuario encontrado: {user.username}")
        if user.check_password(password):
            print("Contraseña correcta")
            return True
        else:
            print("Contraseña incorrecta")
    else:
        print("Usuario no encontrado")
    return False

# Probar con las credenciales del administrador
print("Probando login con credenciales de administrador...")
resultado = probar_login('admin', 'admin123')
print(f"Resultado del login: {'Exitoso' if resultado else 'Fallido'}") 