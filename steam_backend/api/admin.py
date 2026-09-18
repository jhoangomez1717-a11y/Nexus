"""
Archivo: admin.py
Propósito: Configurar el panel de administración de Django (la ruta /admin).
Este archivo registra los modelos de la base de datos para que los administradores 
puedan ver, crear, editar y eliminar registros (juegos, usuarios, reseñas, etc.) 
directamente desde una interfaz web gráfica, sin necesidad de tocar la base de datos.
"""

from django.contrib import admin

# Importamos absolutamente todos los modelos que diseñamos en nuestra arquitectura (models.py)
from .models import (
    UserProfile, Developer, Publisher, Platform, Genre, Game,
    GamePlatform, GameGenre, GameMedia, LibraryItem, UserGameProgress,
    Achievement, UserAchievement, Collection, CollectionItem,
    Review, Wishlist, Transaction, TransactionItem
)

# ==========================================================
# REGISTRO DE MODELOS EN EL PANEL DE CONTROL
# ==========================================================
# El método admin.site.register() inyecta cada modelo en el administrador de Django.
# Si un modelo no se registra aquí, existirá en la base de datos pero será invisible en el panel web.

admin.site.register(UserProfile)
admin.site.register(Developer)
admin.site.register(Publisher)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(GamePlatform)
admin.site.register(GameGenre)
admin.site.register(GameMedia)
admin.site.register(LibraryItem)
admin.site.register(UserGameProgress)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Collection)
admin.site.register(CollectionItem)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Transaction)
admin.site.register(TransactionItem)