"""
Archivo: actualizar_sinopsis.py
Propósito: Bot/Script de automatización (Web Scraping).
Se encarga de buscar en la base de datos todos los juegos que tienen una sinopsis genérica,
se conecta a la API pública de Steam para descargar la descripción real en español, 
limpia el texto de basura HTML y actualiza la base de datos.
"""

import os
import django
import urllib.request
import json
import time
import re
from urllib.error import HTTPError

# ==========================================
# CONFIGURACIÓN DEL ENTORNO DJANGO
# ==========================================
# Permite que este script externo (bot) pueda acceder a los modelos y base de datos
# de Django sin necesidad de encender el servidor web.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "steam_backend.settings")
django.setup()

from api.models import Game

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def limpiar_html(texto_bruto):
    """
    Limpia la basura HTML que a veces envía Steam (ej: <b>, <br>, <i>) 
    usando expresiones regulares, dejando solo el texto puro para nuestra tienda.
    """
    limpiador = re.compile('<.*?>')
    return re.sub(limpiador, '', texto_bruto)

# ==========================================
# LÓGICA PRINCIPAL DEL BOT
# ==========================================
def cazar_todas_las_sinopsis():
    """
    Función principal del bot. Trabaja en bucle hasta que no queden juegos con 
    la sinopsis genérica ("Añadido desde la base").
    Procesa en lotes para cuidar la memoria y respeta los límites de peticiones de Steam.
    """
    # El while mantendrá vivo el script hasta que ya no queden juegos con el texto genérico
    while True:
        juegos_restantes = Game.objects.filter(synopsis__startswith="Añadido desde la base")
        total = juegos_restantes.count()
        
        if total == 0:
            print("✅ ¡Misión cumplida! Todos los juegos tienen su sinopsis real.")
            break
            
        print(f"\n🎮 El bot encontró {total} juegos restantes en la cola. Procesando lote...")
        
        # Tomamos 100 juegos a la vez para no saturar la memoria RAM de la computadora
        lote = juegos_restantes[:100]
        
        for juego in lote:
            try:
                # Extraemos el AppID de Steam desde la URL de la carátula
                appid = juego.cover.split('/')[-2]
                url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=spanish"
                
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    datos = json.loads(response.read().decode('utf-8'))
                    
                # Si Steam devuelve éxito para ese juego, actualizamos la base de datos
                if datos[str(appid)]['success']:
                    juego.synopsis = limpiar_html(datos[str(appid)]['data']['short_description'])
                    juego.save()
                    print(f"✅ [{total}] Actualizado: {juego.title}")
                    total -= 1
                else:
                    # Si Steam ya no tiene info de ese juego, le quitamos la frase de búsqueda para no estancarnos
                    juego.synopsis = f"Descripción no disponible en la tienda. Descubre {juego.title}."
                    juego.save()
                
                # Respetamos el límite de la API de Steam: 1 petición por segundo para evitar baneos
                time.sleep(1)
                
            except HTTPError as e:
                # Manejo específico del Error 429 (Too Many Requests - Demasiadas peticiones)
                if e.code == 429:
                    print("⚠️ Steam detectó velocidad alta (Error 429). El bot dormirá 60 segundos para evitar baneo...")
                    time.sleep(60)
                else:
                    juego.synopsis = f"Error al cargar sinopsis. Descubre {juego.title}."
                    juego.save()
            except Exception as e:
                # Respaldo general ante cualquier otro error de conexión o lectura
                juego.synopsis = f"Error al cargar sinopsis. Descubre {juego.title}."
                juego.save()

# Punto de entrada del script
if __name__ == "__main__":
    cazar_todas_las_sinopsis()