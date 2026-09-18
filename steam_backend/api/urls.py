"""
Archivo: urls.py
Propósito: Define el enrutamiento (los endpoints o URLs) de la API REST.
Conecta las solicitudes HTTP que llegan desde Angular (ej: GET a /api/games/) 
con la función específica en views.py que debe procesar esa petición.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importamos las vistas (ViewSets) y la función de registro que procesarán las peticiones
from .views import (
    UserProfileViewSet, DeveloperViewSet, PublisherViewSet,
    PlatformViewSet, GenreViewSet, GameViewSet,
    LibraryItemViewSet, ReviewViewSet, WishlistViewSet, CollectionViewSet,
    register_user  # Función personalizada para el registro de nuevas cuentas
)

# ==========================================
# ENRUTADOR AUTOMÁTICO (ROUTER)
# ==========================================
# DefaultRouter genera automáticamente todas las rutas estándar (GET, POST, PUT, DELETE)
# para cada ViewSet registrado. Esto nos ahorra escribir decenas de rutas manualmente.
router = DefaultRouter()

# Registramos los endpoints de la API. 
# Ej: router.register(r'games', GameViewSet) crea las rutas /api/games/ y /api/games/<id>/
router.register(r'profiles', UserProfileViewSet)
router.register(r'developers', DeveloperViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'games', GameViewSet)
router.register(r'library', LibraryItemViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'wishlist', WishlistViewSet)
router.register(r'collections', CollectionViewSet)

# ==========================================
# LISTA FINAL DE URLs (URLPATTERNS)
# ==========================================
urlpatterns = [
    # Incluimos todas las rutas automáticas generadas por el Router en la raíz de esta app
    path('', include(router.urls)),
    
    # Ruta manual y específica para la creación de nuevos usuarios
    # Se accede enviando un POST a /api/register/
    path('register/', register_user, name='register'),
]