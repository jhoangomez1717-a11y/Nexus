"""
Archivo: models.py
Propósito: Define la arquitectura de la base de datos de NEXUS (ORM de Django).
Aquí se estructuran todas las tablas (modelos) y sus relaciones (Uno a Uno, Uno a Muchos, Muchos a Muchos) 
para gestionar usuarios, el catálogo de juegos, la biblioteca personal, los logros y las transacciones.
"""

from django.db import models
from django.contrib.auth.models import User

# ==========================================
# MÓDULO 1: USUARIOS Y PERFILES
# ==========================================
class UserProfile(models.Model):
    """
    Extiende el modelo User nativo de Django (relación 1 a 1).
    Almacena datos adicionales del jugador como su saldo en la billetera, avatar y país.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


# ==========================================
# MÓDULO 2: CATÁLOGO DE JUEGOS Y TIENDA
# ==========================================
class Developer(models.Model):
    """Tabla para los estudios desarrolladores de los videojuegos."""
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    """Tabla para las empresas distribuidoras/editoras de los juegos."""
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

class Platform(models.Model):
    """Plataformas en las que un juego está disponible (PC, Mac, Linux, etc.)."""
    name = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.name

class Genre(models.Model):
    """Categorías o géneros de los videojuegos (Acción, RPG, Indie, etc.)."""
    name = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.name

class Game(models.Model):
    """
    Modelo central del catálogo.
    Contiene la información principal de cada videojuego y sus relaciones 
    con desarrolladores, distribuidores, plataformas y géneros.
    """
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    release_date = models.DateField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, related_name='games')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='games')
    platforms = models.ManyToManyField(Platform, through='GamePlatform')
    genres = models.ManyToManyField(Genre, through='GameGenre')
    cover = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class GamePlatform(models.Model):
    """Tabla intermedia (Muchos a Muchos) que vincula un Juego con una Plataforma específica y su precio."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    digital_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('game', 'platform')

class GameGenre(models.Model):
    """Tabla intermedia (Muchos a Muchos) que vincula un Juego con sus Géneros."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('game', 'genre')

class GameMedia(models.Model):
    """Almacena imágenes o videos promocionales asociados a un juego específico."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=50) # 'image' o 'video'
    file_url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.game.title} - {self.media_type}"


# ==========================================
# MÓDULO 3: BIBLIOTECA, PROGRESO Y LOGROS
# ==========================================
class LibraryItem(models.Model):
    """
    Representa un juego adquirido por un usuario.
    Registra cuándo lo compró, cuánto tiempo lo ha jugado y su última sesión.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    playtime_minutes = models.IntegerField(default=0)
    last_played_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

class UserGameProgress(models.Model):
    """Rastrea el estado de completitud de un juego dentro de la biblioteca de un usuario."""
    library_item = models.OneToOneField(LibraryItem, on_delete=models.CASCADE, related_name='progress')
    status = models.CharField(max_length=50, default='Pendiente') # Jugando, Completado, Pendiente, Abandonado
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.library_item} ({self.status})"

class Achievement(models.Model):
    """Define los logros globales disponibles para desbloquear en un juego específico."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.game.title}: {self.title}"

class UserAchievement(models.Model):
    """Tabla intermedia que registra cuándo un usuario desbloquea un logro específico."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')


# ==========================================
# MÓDULO 4: ORGANIZACIÓN, RESEÑAS Y SOCIAL
# ==========================================
class Collection(models.Model):
    """Permite a los usuarios crear carpetas personalizadas (ej. 'Favoritos') para organizar su biblioteca."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class CollectionItem(models.Model):
    """Asocia juegos específicos de la biblioteca a una colección personalizada."""
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    library_item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('collection', 'library_item')

class Review(models.Model):
    """Sistema de reseñas y calificaciones dejadas por los usuarios sobre los juegos que poseen."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField() # 1 a 5 o 1 a 10
    comment = models.TextField()
    recommended = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"Review by {self.user.username} on {self.game.title}"

class Wishlist(models.Model):
    """Lista de deseos para que los usuarios guarden juegos que planean comprar a futuro."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')


# ==========================================
# MÓDULO 5: TRANSACCIONES Y CARRITO
# ==========================================
class Transaction(models.Model):
    """Registra la cabecera de una compra (el total pagado, método de pago y estado de la orden)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Completado')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx #{self.id} - {self.user.username}"

class TransactionItem(models.Model):
    """Detalle de factura: registra individualmente cada juego comprado dentro de una transacción."""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Tx #{self.transaction.id} - {self.game.title}"