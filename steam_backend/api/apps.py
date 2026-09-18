"""
Archivo: apps.py
Propósito: Archivo de configuración principal de la aplicación.
Le indica al núcleo del proyecto Django cómo se llama esta aplicación 
y permite configurar comportamientos específicos al momento de que la app arranque.
"""

from django.apps import AppConfig

class ApiConfig(AppConfig):
    """
    Clase de configuración para la aplicación 'api'.
    Hereda de AppConfig, que es la clase base de Django para registrar aplicaciones.
    """
    
    # Define el nombre interno que Django usará para identificar esta aplicación.
    # Este es el nombre que se agrega en la lista INSTALLED_APPS del archivo settings.py.
    name = 'api'