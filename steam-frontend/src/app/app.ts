/**
 * Archivo: app.ts
 * Propósito: Controlador (Lógica TypeScript) del componente principal de la aplicación.
 * Define el comportamiento de la estructura base (Navbar). Se encarga de verificar el estado 
 * de la sesión del usuario accediendo al almacenamiento local (localStorage) 
 * y maneja la acción de cerrar sesión.
 */
import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root', // Nombre de la etiqueta HTML donde se inyectará este componente
  standalone: true,     // Indica que usa la arquitectura moderna sin NgModules
  imports: [RouterOutlet, RouterLink, RouterLinkActive, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css' // Si no usas app.css, simplemente borra esta línea
})
export class AppComponent {
  
  // Esto verifica si tienes la "Pulsera VIP" guardada
  // Retorna un booleano (true/false) determinando si el usuario inició sesión
  get isLogged(): boolean {
    return !!localStorage.getItem('nexus_token');
  }

  // Esto recupera tu nombre (ej. Jhoan17) para mostrarlo en la interfaz
  get username(): string {
    return localStorage.getItem('nexus_username') || '';
  }

  // Función para cerrar sesión
  // Limpia los datos locales del navegador para destruir la sesión y redirige al inicio
  logout(): void {
    localStorage.removeItem('nexus_token');
    localStorage.removeItem('nexus_username');
    window.location.href = '/login'; // Recarga la página y te saca
  }
}