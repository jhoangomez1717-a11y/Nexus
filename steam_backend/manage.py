"""
Archivo: manage.py
Propósito: Es el punto de entrada principal para interactuar con el proyecto desde la terminal.
Actúa como un "controlador de comandos" (CLI). Es el script que recibe las órdenes que escribes 
en la consola (como 'runserver', 'makemigrations' o 'migrate') y se encarga de ejecutarlas 
dentro del entorno del proyecto.
Por convención, los desarrolladores nunca modifican este archivo.
"""

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # 1. Le indica a Python dónde están las configuraciones globales (settings.py) 
    # de tu proyecto 'steam_backend' para que pueda cargar la base de datos y las apps.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steam_backend.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado o olvidaste activar tu entorno virtual (venv), 
        # el script lanza este error para avisarte.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 2. Toma lo que escribiste en la terminal (sys.argv) y lo ejecuta.
    # Por ejemplo, si escribes 'python manage.py runserver', sys.argv toma la palabra 'runserver'.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()