"""
Archivo: views.py
Propósito: Contiene la lógica de negocio y los controladores de la API.
Aquí se define qué datos se envían cuando Angular solicita información (GET) 
y cómo se procesan los datos que Angular envía (POST/PUT).
Utiliza ViewSets para generar automáticamente operaciones CRUD (Crear, Leer, Actualizar, Borrar).
"""

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
import urllib.request
import json
import re
from rest_framework import viewsets, filters
from rest_framework.response import Response

# Importamos todos los Modelos y Serializadores necesarios
from .models import (
    UserProfile, Developer, Publisher, Platform, Genre, Game,
    GamePlatform, GameGenre, GameMedia, LibraryItem, UserGameProgress,
    Achievement, UserAchievement, Collection, CollectionItem,
    Review, Wishlist, Transaction, TransactionItem
)
from .serializers import (
    UserProfileSerializer, DeveloperSerializer, PublisherSerializer,
    PlatformSerializer, GenreSerializer, GameSerializer,
    LibraryItemSerializer, ReviewSerializer, WishlistSerializer,
    CollectionSerializer
)

# ==========================================
# VISTAS AUTOMÁTICAS (CRUD BÁSICO)
# ==========================================
# Estas clases generan automáticamente los endpoints para gestionar sus respectivos modelos.

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class LibraryItemViewSet(viewsets.ModelViewSet):
    queryset = LibraryItem.objects.all()
    serializer_class = LibraryItemSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


# ==========================================
# VISTA PRINCIPAL DEL CATÁLOGO (CON OPTIMIZACIÓN)
# ==========================================
class GameViewSet(viewsets.ModelViewSet):
    """
    Controla el catálogo de juegos de la tienda.
    Utiliza 'select_related' para optimizar la base de datos (evita el problema N+1 consultas),
    y configura los campos por los cuales Angular puede buscar juegos (título, género, desarrollador).
    """
    queryset = Game.objects.select_related('developer').all().order_by('-release_date')
    serializer_class = GameSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genres__name', 'developer__name']


# ==========================================
# VISTA DE RESEÑAS (CON WEB SCRAPING A STEAM)
# ==========================================
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Controla las reseñas de los juegos.
    Si un juego no tiene reseñas locales en la base de datos, 
    esta vista se conecta en tiempo real a la API pública de Steam,
    descarga reseñas reales del juego, las limpia y se las envía a Angular.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        # 1. Obtenemos el ID del juego que el usuario está mirando
        game_id = request.query_params.get('game')
        
        if game_id and game_id != 'undefined':
            # 2. Buscamos primero si hay reseñas guardadas en nuestra propia base de datos (NEXUS)
            reviews = Review.objects.filter(game_id=game_id).order_by('-id')
            
            if reviews.exists():
                page = self.paginate_queryset(reviews)
                if page is not None:
                    return self.get_paginated_response(self.get_serializer(page, many=True).data)
                return Response(self.get_serializer(reviews, many=True).data)
            
            # 3. Si no hay reseñas locales, consultamos la API de Steam
            virtual_reviews = []
            try:
                game = Game.objects.get(id=game_id)
                # Extraemos el AppID de Steam desde la URL de la carátula usando una expresión regular
                match = re.search(r'/apps/(\d+)/', game.cover) if game.cover else None
                
                if match:
                    appid = match.group(1)
                    # Solicitamos reseñas en español directamente a Steam
                    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=spanish&purchase_type=all"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    with urllib.request.urlopen(req) as response:
                        data = json.loads(response.read().decode('utf-8'))
                        if 'reviews' in data:
                            # Tomamos las primeras 10 reseñas
                            for idx, item in enumerate(data['reviews'][:10]):
                                # Limpiamos las etiquetas de formato que usa Steam ([b], [/b])
                                texto_limpio = item.get('review', '').replace('[b]', '').replace('[/b]', '')
                                virtual_reviews.append({
                                    'id': 1000 + idx,
                                    'comment': texto_limpio,
                                    'rating': 5 if item.get('voted_up') else 1,
                                    'game': game.id
                                })
            except Exception as e:
                print(f"Error conectando a Steam: {e}")

            # 4. Plan de respaldo: si no hay internet o Steam falla, generamos una reseña falsa para no dejar el espacio en blanco
            if not virtual_reviews:
                virtual_reviews.append({
                    'id': 9999,
                    'comment': "¡Una joya oculta! Totalmente recomendado por la comunidad de NEXUS.",
                    'rating': 5,
                    'game': int(game_id)
                })

            # 5. Empaquetamos las reseñas de Steam simulando la estructura que genera Django
            return Response({
                'count': len(virtual_reviews),
                'next': None,
                'previous': None,
                'results': virtual_reviews
            })

        return super().list(request, *args, **kwargs)


# ==========================================
# REGISTRO DE NUEVOS USUARIOS
# ==========================================
@api_view(['POST'])
@permission_classes([AllowAny]) # Permite que cualquier persona (sin estar logueada) acceda a esta ruta
def register_user(request):
    """
    Endpoint personalizado para crear cuentas nuevas.
    Recibe el usuario y contraseña desde el formulario de Angular, valida que el nombre 
    no esté ocupado, y registra al usuario en la base de datos de Django de forma segura.
    """
    username = request.data.get('username')
    email = request.data.get('email', '')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe, elige otro nombre'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Creamos el usuario asegurando la encriptación de la contraseña
    User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'Cuenta creada con éxito'}, status=status.HTTP_201_CREATED)