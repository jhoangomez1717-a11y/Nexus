/**
 * Archivo: app.config.ts
 * Propósito: Configuración global y raíz de la aplicación Angular (Frontend).
 * Como NEXUS utiliza la arquitectura moderna "Standalone Components" de Angular,
 * este archivo reemplaza al tradicional app.module.ts.
 * Aquí inyectamos los servicios y módulos esenciales que toda la aplicación necesita para funcionar.
 */

import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    // Captura y maneja los errores globales en el navegador para evitar que la interfaz colapse
    provideBrowserGlobalErrorListeners(),
    
    // Inyecta el sistema de navegación basado en las rutas que definimos en app.routes.ts
    provideRouter(routes),
    
    // IMPORTANTE: Inyecta HttpClient, la herramienta vital que nos permite hacer 
    // peticiones HTTP (GET, POST) a nuestra base de datos y backend en Django.
    provideHttpClient()
  ]
};