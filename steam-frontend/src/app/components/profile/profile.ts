/**
 * Archivo: profile.ts
 * Propósito: Controlador (Lógica TypeScript) del componente del Perfil de Usuario.
 * Gestiona la carga de la actividad reciente del jugador desde el LocalStorage y 
 * ejecuta la lógica matemática para calcular dinámicamente el "Nivel de Cuenta" 
 * y las "Insignias" basándose en el tamaño de la biblioteca y los logros obtenidos.
 */

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class ProfileComponent implements OnInit {
  // ==========================================
  // VARIABLES DE ESTADO Y PROGRESIÓN
  // ==========================================
  username: string = '';
  level: number = 1;  // 👈 Empezamos en nivel 1 por defecto
  badges: number = 0; // 👈 Empezamos con 0 insignias por defecto
  recentGames: any[] = [];
  totalGames: number = 0;

  // ==========================================
  // CICLO DE VIDA DEL COMPONENTE
  // ==========================================
  /**
   * Se ejecuta al inicializar el componente.
   * Rescata el nombre del usuario de la sesión actual y llama a la función
   * encargada de cargar y calcular todas las estadísticas del perfil.
   */
  ngOnInit(): void {
    this.username = localStorage.getItem('nexus_username') || 'Usuario';
    this.loadProfileData();
  }

  // ==========================================
  // LÓGICA DE NEGOCIO Y CÁLCULO DE ESTADÍSTICAS
  // ==========================================
  /**
   * Lee la biblioteca de juegos del usuario, suma los logros totales obtenidos 
   * y aplica un algoritmo para definir el nivel y las insignias de la cuenta.
   */
  loadProfileData(): void {
    if (!this.username) return;
    
    // Obtiene la colección personal del usuario usando su clave única
    const libraryKey = `nexus_library_${this.username}`;
    const library = JSON.parse(localStorage.getItem(libraryKey) || '[]');
    
    // Asigna los juegos a la variable que alimenta la vista HTML
    this.recentGames = library;
    this.totalGames = library.length;

    // Recorre todos los juegos comprados para sumar cuántos logros ha desbloqueado en total
    let totalAchievements = 0;
    library.forEach((game: any) => {
      totalAchievements += (game.achievementsUnlocked || 0);
    });

    // 🪄 SISTEMA DE NIVELACIÓN DINÁMICO (ALGORITMO DE PROGRESIÓN)
    if (this.totalGames === 0) {
      // Si la cuenta es nueva y no tiene juegos comprados, se mantienen los valores base
      this.level = 1;
      this.badges = 0;
    } else {
      // CÁLCULO DE NIVEL:
      // Nivel 1 base + 1 nivel por cada juego comprado + 1 nivel extra por cada 5 logros desbloqueados
      this.level = 1 + this.totalGames + Math.floor(totalAchievements / 5);
      
      // CÁLCULO DE INSIGNIAS:
      // 1 insignia base por ser comprador activo + 1 insignia extra por cada 10 logros acumulados
      this.badges = 1 + Math.floor(totalAchievements / 10);
    }
  }

  /**
   * Calcula el porcentaje de completitud de un juego individual.
   * Se usa en el HTML para renderizar la longitud de la barra roja de progreso.
   */
  getAchievementPercentage(game: any): number {
    if (!game || game.totalAchievements === 0) return 0;
    return (game.achievementsUnlocked / game.totalAchievements) * 100;
  }
}