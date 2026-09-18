"""
Archivo: poblar.py
Propósito: Script de automatización para la inyección masiva de datos (Data Seeding).
Se conecta a la API pública de SteamSpy para descargar información real de cientos de videojuegos 
(títulos, desarrolladores, precios) y poblar automáticamente la base de datos de NEXUS.
Evita el trabajo manual de registrar juegos uno por uno en el panel de administrador.
"""

import os
import django
import urllib.request
import json
import random
from datetime import date, timedelta
import time

# ==========================================
# CONFIGURACIÓN DEL ENTORNO DJANGO
# ==========================================
# Prepara el entorno para que este script independiente pueda interactuar con la base de datos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "steam_backend.settings")
django.setup()

from api.models import Game, Developer, Publisher, Genre

# ==========================================
# LÓGICA DE POBLACIÓN MASIVA
# ==========================================
def poblar_masivo():
    """
    Descarga datos de SteamSpy en lotes (páginas) y construye los registros en la base de datos.
    Si un desarrollador, distribuidor o juego ya existe, lo omite para evitar duplicados.
    """
    print("Iniciando inyección de escala masiva (500 juegos)...")
    
    # 1. Aseguramos que existan al menos tres géneros base en la tienda
    g_accion, _ = Genre.objects.get_or_create(name="Acción")
    g_rpg, _ = Genre.objects.get_or_create(name="RPG")
    g_indie, _ = Genre.objects.get_or_create(name="Indie")
    
    juegos_creados = 0
    
    # 2. Recorremos 5 páginas de la API de SteamSpy (Cada página trae 100 juegos)
    for pagina in range(5):
        print(f"Descargando lote {pagina + 1} de 5 desde la API global...")
        url = f"https://steamspy.com/api.php?request=all&page={pagina}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            datos_api = json.loads(response.read().decode())
            
        # 3. Procesamos cada juego recibido en el JSON
        for appid, info in datos_api.items():
            titulo = info.get("name", "Desconocido")
            dev_name = info.get("developer") or "Desarrollador Independiente"
            pub_name = info.get("publisher") or "Editor Independiente"
            
            # get_or_create busca el registro; si no existe, lo crea automáticamente
            dev_obj, _ = Developer.objects.get_or_create(name=dev_name[:250])
            pub_obj, _ = Publisher.objects.get_or_create(name=pub_name[:250])
            
            # 4. Conversión de precios simulada (centavos de dólar a pesos colombianos aproximados)
            precio_centavos = info.get("price", 0)
            precio_cop = float(precio_centavos) * 40.0 if precio_centavos else random.choice([0, 35000, 90000])

            # 5. Creación del juego en nuestra base de datos (NEXUS)
            juego, creado = Game.objects.get_or_create(
                title=titulo,
                defaults={
                    # Esta sinopsis temporal luego será reemplazada por el bot actualizar_sinopsis.py
                    "synopsis": f"Añadido desde la base de datos global de Steam. Descubre {titulo}.",
                    "base_price": precio_cop,
                    "release_date": date.today() - timedelta(days=random.randint(100, 4000)),
                    "developer": dev_obj,
                    "publisher": pub_obj,
                    # Construimos la URL de la imagen usando el AppID oficial de Steam
                    "cover": f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg"
                }
            )
            
            # 6. Si el juego es nuevo, le asignamos un género al azar
            if creado:
                juego.genres.set([random.choice([g_accion, g_rpg, g_indie])])
                juegos_creados += 1
        
        # 7. Respetamos el límite de peticiones del servidor de SteamSpy
        time.sleep(1.5)
        
    print(f"\n¡Éxito total! Se forjaron {juegos_creados} juegos nuevos en NEXUS.")

if __name__ == "__main__":
    poblar_masivo()