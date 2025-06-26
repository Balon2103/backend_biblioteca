#!/usr/bin/env python3
"""
Script de prueba para verificar el footer
"""

import requests
import re

def test_footer():
    try:
        # Hacer una petición al servidor
        response = requests.get('http://127.0.0.1:5000/', timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Buscar el email en el contenido
            if 'bibliotecajmd.fupagua@gmail.com' in content:
                print("✅ Email encontrado en el footer")
            else:
                print("❌ Email NO encontrado en el footer")
                
            # Buscar la ciudad
            if 'Ciudad San Juan de los Morros' in content:
                print("✅ Ciudad encontrada en el footer")
            else:
                print("❌ Ciudad NO encontrada en el footer")
                
            # Buscar la sección de contacto
            if 'footer-contact' in content:
                print("✅ Sección de contacto encontrada")
            else:
                print("❌ Sección de contacto NO encontrada")
                
        else:
            print(f"❌ Error en la respuesta del servidor: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está corriendo en http://127.0.0.1:5000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 Verificando el footer...")
    test_footer() 