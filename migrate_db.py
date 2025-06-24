from main import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Agregar columna portada_url si no existe
            db.session.execute(text('ALTER TABLE libros ADD COLUMN portada_url VARCHAR(500)'))
            db.session.commit()
            print("Migración completada exitosamente")
        except Exception as e:
            print(f"Error durante la migración: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    migrate() 