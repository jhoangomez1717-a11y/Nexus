/**
 * Archivo: main.ts
 * Propósito: Punto de entrada principal (Entry Point) de la aplicación Angular.
 * Es el primer archivo TypeScript que se compila y ejecuta cuando la página carga.
 * Su única función es inicializar (bootstrap) el componente raíz (AppComponent)
 * inyectándole todas las configuraciones globales definidas en appConfig.
 */
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));