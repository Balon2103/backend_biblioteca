import pandas as pd
from app import db
from models import Libro  # Asegúrate de que la clase Libro esté correctamente importada

# Lee el archivo de Excel
datos = pd.read_excel('Inventario Bibliográfico.xlsx')  # Usa el nombre correcto del archivo

# Recorre cada fila del archivo
for index, row in datos.iterrows():
    if pd.isna(row['Título']):  # Si el título está vacío, saltamos esta fila
        continue

    nuevo_libro = Libro(
        titulo=row['Título'],
        autor=row['Autor'],
        editorial=row['Editorial'],
        anio=row['Año de edicion'],
        isbn=row['COTA'],  # Si tienes un campo ISBN, usa el adecuado; de lo contrario, usa 'COTA'
        ciudad=row['Ciudad'],
        coleccion=row['Colección'],
        materias=row['Materias'],
        caracteristicas=row['Caract.Formato'],
        cant_ejemplares=row['Cant. Ejemplares'],
        tomos=row['Tomos'],
        medidas=row['Medidas'],
        num_paginas=row['Num. Paginas'],
        verificacion=row['Verificación'],
        disponible=True
    )

    # Agrega el libro a la base de datos
    db.session.add(nuevo_libro)

# Guarda los cambios en la base de datos
db.session.commit()

print("Datos importados correctamente.")
