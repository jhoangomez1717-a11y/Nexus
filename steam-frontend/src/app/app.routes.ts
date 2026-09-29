/**
 * Archivo: app.routes.ts
 * Propósito: Definir el sistema de navegación (Routing) de la aplicación.
 * Mapea cada URL que el usuario escribe en el navegador con el componente visual 
 * (pantalla) que Angular debe mostrar internamente.
 * Convierte a NEXUS en una SPA (Single Page Application) real, permitiendo navegar 
 * sin que la página del navegador tenga que recargarse.
 */

import { Routes } from '@angular/router';

// Importamos todas las "pantallas" o vistas principales de nuestra tienda
import { GameListComponent } from './components/game-list/game-list';
import { AuthComponent } from './components/auth/auth';
import { ProfileComponent } from './components/profile/profile';
import { LibraryComponent } from './components/library/library';

export const routes: Routes = [
  // 1. RUTA RAÍZ (POR DEFECTO): Si el usuario entra a la URL base (ej. localhost:4201/)
  // lo redirigimos automáticamente a la ruta '/tienda'. 
  // pathMatch: 'full' asegura que aplique solo cuando la ruta esté completamente vacía.
  { path: '', redirectTo: '/tienda', pathMatch: 'full' },
  
  // 2. RUTAS DE COMPONENTES: Asocian un segmento de la URL con su respectivo componente.
  // Cuando la URL coincida, Angular inyectará el componente dentro del <router-outlet> en app.html.
  { path: 'tienda', component: GameListComponent },      // Muestra el catálogo principal
  { path: 'login', component: AuthComponent },           // Muestra el formulario de acceso/registro
  { path: 'perfil', component: ProfileComponent },       // Muestra el perfil dinámico y nivel
  { path: 'biblioteca', component: LibraryComponent },   // Muestra los juegos adquiridos
];