from app import app
import pandas as pd
from models import Libro, Usuario, Prestamo
from extensions import db

def importar_libros():
    print("Leyendo archivo Excel...")
    df = pd.read_excel('Inventario Bibliografico.xlsx')
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    
    print("\nInformación del DataFrame:")
    print(df.info())
    
    print("\nTotal de registros en el Excel:", len(df))
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Primero, verificamos si ya hay libros en la base de datos
        libros_existentes = Libro.query.count()
        if libros_existentes > 0:
            print(f"\nYa existen {libros_existentes} libros en la base de datos.")
            return
        
        contador = 0
        saltados = 0
        
        for index, row in df.iterrows():
            if pd.isna(row['Título']) and pd.isna(row['Autor']):
                saltados += 1
                continue
                
            libro = Libro(
                titulo=str(row['Título']).strip() if not pd.isna(row['Título']) else None,
                autor=str(row['Autor']).strip() if not pd.isna(row['Autor']) else None,
                cota=str(row['COTA']).strip() if not pd.isna(row['COTA']) else None,
                editorial=str(row['Editorial']).strip() if not pd.isna(row['Editorial']) else None,
                anio_edicion=str(row['Año de edicion']).strip() if not pd.isna(row['Año de edicion']) else None,
                ciudad=str(row['Ciudad']).strip() if not pd.isna(row['Ciudad']) else None,
                coleccion=str(row['Colección']).strip() if not pd.isna(row['Colección']) else None,
                medidas=str(row['Medidas']).strip() if not pd.isna(row['Medidas']) else None,
                num_paginas=str(row['Num. Paginas']).strip() if not pd.isna(row['Num. Paginas']) else None,
                caract_formato=str(row['Caract.Formato']).strip() if not pd.isna(row['Caract.Formato']) else None,
                cant_ejemplares=str(row['Cant. Ejemplares']).strip() if not pd.isna(row['Cant. Ejemplares']) else None,
                tomos=str(row['Tomos']).strip() if not pd.isna(row['Tomos']) else None,
                verificacion=str(row['Verificación']).strip() if not pd.isna(row['Verificación']) else None,
                materias=str(row['Materias']).strip() if not pd.isna(row['Materias']) else None,
                disponible=True  # Establecer todos los libros como disponibles por defecto
            )
            
            db.session.add(libro)
            contador += 1
            
            if contador % 100 == 0:
                print(f"Procesados {contador} registros...")
                db.session.commit()  # Commit cada 100 registros
        
        # Commit final para los registros restantes
        db.session.commit()
        
        print("\nImportación completada exitosamente")
        print(f"Se importaron {contador} registros")
        print(f"Se saltaron {saltados} registros sin título ni autor")
        
        # Verificar la importación
        total_libros = Libro.query.count()
        print(f"Total de libros en la base de datos: {total_libros}")
        
        print("\nPrimeros 3 registros de la base de datos:")
        primeros_libros = Libro.query.limit(3).all()
        for libro in primeros_libros:
            print(f"\nID: {libro.id}")
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Editorial: {libro.editorial}")
            print(f"Año: {libro.anio_edicion}")
            print(f"Páginas: {libro.num_paginas}")
            print(f"Ejemplares: {libro.cant_ejemplares}")
            print(f"Disponible: {libro.disponible}")

if __name__ == '__main__':
    importar_libros() 