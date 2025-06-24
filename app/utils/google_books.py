import requests
from typing import Optional
import re
from datetime import datetime

def limpiar_texto(texto: str) -> str:
    """Limpia el texto eliminando caracteres especiales y normalizando espacios."""
    if not texto:
        return ""
    # Eliminar caracteres especiales y normalizar espacios
    texto_limpio = re.sub(r'[^\w\s]', '', texto)
    return ' '.join(texto_limpio.split())

def extraer_anio(fecha: str) -> Optional[str]:
    """Extrae el año de una fecha en formato string."""
    if not fecha:
        return None
    # Intentar extraer el año usando diferentes patrones
    patrones = [
        r'\b\d{4}\b',  # Año de 4 dígitos
        r'\b19\d{2}\b',  # Años 1900-1999
        r'\b20\d{2}\b'   # Años 2000-2099
    ]
    
    for patron in patrones:
        match = re.search(patron, fecha)
        if match:
            return match.group()
    return None

def buscar_portada_libro(isbn: str = None, titulo: str = None, autor: str = None, editorial: str = None, anio: str = None) -> Optional[str]:
    """
    Busca la portada de un libro usando la API de Google Books.
    
    Args:
        isbn: ISBN del libro
        titulo: Título del libro
        autor: Autor del libro
        editorial: Editorial del libro
        anio: Año de publicación
        
    Returns:
        URL de la portada del libro o None si no se encuentra
    """
    base_url = "https://www.googleapis.com/books/v1/volumes"
    
    # Construir la consulta
    query_parts = []
    if isbn:
        # Limpiar el ISBN de guiones y espacios
        isbn_limpio = re.sub(r'[-\s]', '', isbn)
        query_parts.append(f"isbn:{isbn_limpio}")
    if titulo:
        query_parts.append(f"intitle:{limpiar_texto(titulo)}")
    if autor:
        query_parts.append(f"inauthor:{limpiar_texto(autor)}")
    if editorial:
        query_parts.append(f"inpublisher:{limpiar_texto(editorial)}")
    
    query = " ".join(query_parts)
    
    try:
        response = requests.get(f"{base_url}?q={query}&maxResults=5")
        response.raise_for_status()
        data = response.json()
        
        if data.get("totalItems", 0) > 0:
            mejor_coincidencia = None
            mejor_puntuacion = 0
            
            for item in data["items"]:
                book = item["volumeInfo"]
                puntuacion = 0
                
                # Verificar coincidencia de ISBN
                if isbn and "industryIdentifiers" in book:
                    for identifier in book["industryIdentifiers"]:
                        id_value = re.sub(r'[-\s]', '', identifier.get("identifier", ""))
                        if id_value == isbn_limpio:
                            puntuacion += 5  # Aumentar peso del ISBN
                            break
                
                # Verificar coincidencia de título
                if titulo and "title" in book:
                    titulo_limpio = limpiar_texto(titulo)
                    titulo_libro = limpiar_texto(book["title"])
                    if titulo_limpio.lower() == titulo_libro.lower():
                        puntuacion += 4  # Coincidencia exacta
                    elif titulo_limpio.lower() in titulo_libro.lower():
                        puntuacion += 2  # Coincidencia parcial
                
                # Verificar coincidencia de autor
                if autor and "authors" in book:
                    autor_limpio = limpiar_texto(autor)
                    for a in book["authors"]:
                        if autor_limpio.lower() == limpiar_texto(a).lower():
                            puntuacion += 3  # Coincidencia exacta
                        elif autor_limpio.lower() in limpiar_texto(a).lower():
                            puntuacion += 1  # Coincidencia parcial
                
                # Verificar coincidencia de año
                if anio and "publishedDate" in book:
                    anio_libro = extraer_anio(book["publishedDate"])
                    if anio_libro and anio in anio_libro:
                        puntuacion += 2
                
                # Si tiene imagen y mejor puntuación, actualizar mejor coincidencia
                if "imageLinks" in book and puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    if "extraLarge" in book["imageLinks"]:
                        mejor_coincidencia = book["imageLinks"]["extraLarge"]
                    elif "large" in book["imageLinks"]:
                        mejor_coincidencia = book["imageLinks"]["large"]
                    elif "thumbnail" in book["imageLinks"]:
                        mejor_coincidencia = book["imageLinks"]["thumbnail"].replace("zoom=1", "zoom=2")
                    elif "smallThumbnail" in book["imageLinks"]:
                        mejor_coincidencia = book["imageLinks"]["smallThumbnail"].replace("zoom=1", "zoom=2")
            
            # Solo devolver la coincidencia si tiene una puntuación mínima
            if mejor_puntuacion >= 3:
                return mejor_coincidencia
        
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar la portada: {str(e)}")
        return None
    except Exception as e:
        print(f"Error inesperado al buscar la portada: {str(e)}")
        return None 