"""
Archivo: serializers.py
Propósito: Funciona como el "traductor" de la API (Django REST Framework).
Su trabajo es tomar los datos complejos de la base de datos (objetos de Python de models.py) 
y convertirlos en formato JSON para que el frontend en Angular pueda leerlos fácilmente. 
También hace el proceso inverso: recibe JSON de Angular y lo valida antes de guardarlo en la base de datos.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Developer, Publisher, Platform, Genre, Game,
    GamePlatform, GameGenre, GameMedia, LibraryItem, UserGameProgress,
    Achievement, UserAchievement, Collection, CollectionItem,
    Review, Wishlist, Transaction, TransactionItem
)

# ==========================================
# SERIALIZADORES DE USUARIO
# ==========================================
class UserSerializer(serializers.ModelSerializer):
    """Convierte el modelo nativo User de Django. Solo exponemos campos seguros (id, username, email)."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializa el perfil extendido del usuario. 
    Usa 'read_only=True' para anidar los datos del User nativo dentro del perfil 
    sin permitir que se modifiquen desde este endpoint.
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'


# ==========================================
# SERIALIZADORES DE METADATOS (CATÁLOGO)
# ==========================================
class DeveloperSerializer(serializers.ModelSerializer):
    """Convierte los datos de los desarrolladores a JSON."""
    class Meta:
        model = Developer
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    """Convierte los datos de los distribuidores a JSON."""
    class Meta:
        model = Publisher
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    """Convierte las plataformas disponibles a JSON."""
    class Meta:
        model = Platform
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    """Convierte los géneros de videojuegos a JSON."""
    class Meta:
        model = Genre
        fields = '__all__'

class GameMediaSerializer(serializers.ModelSerializer):
    """Convierte las URLs de imágenes y videos promocionales a JSON."""
    class Meta:
        model = GameMedia
        fields = '__all__'


# ==========================================
# SERIALIZADOR PRINCIPAL: JUEGOS
# ==========================================
class GameSerializer(serializers.ModelSerializer):
    """
    Es el serializador más pesado e importante de la tienda.
    Anida (incluye) los serializadores de Developer, Publisher, Genre, Platform y Media.
    Esto permite que Angular reciba toda la información del juego en una sola petición (JSON anidado),
    en lugar de recibir solo números (IDs) y tener que hacer múltiples consultas.
    """
    developer = DeveloperSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    media = GameMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'


# ==========================================
# SERIALIZADORES DE INTERACCIÓN DEL USUARIO
# ==========================================
class LibraryItemSerializer(serializers.ModelSerializer):
    """
    Serializa los juegos adquiridos por un usuario.
    Anida 'GameSerializer' para que la biblioteca en Angular pueda mostrar las carátulas y títulos reales.
    """
    game = GameSerializer(read_only=True)
    class Meta:
        model = LibraryItem
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializa las reseñas de la comunidad. 
    Anida 'UserSerializer' para mostrar quién escribió la reseña (autor).
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    """Serializa la lista de deseos de un usuario, anidando la información del juego."""
    game = GameSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    """Serializa las colecciones/carpetas personalizadas creadas por el usuario."""
    class Meta:
        model = Collection
        fields = '__all__'