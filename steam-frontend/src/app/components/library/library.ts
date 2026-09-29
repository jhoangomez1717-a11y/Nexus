/**
 * Archivo: library.ts
 * Propósito: Controlador (Lógica TypeScript) del componente de la Biblioteca.
 * Gestiona el inventario personal de juegos del usuario, cargándolos desde el 
 * almacenamiento local (LocalStorage). Además, implementa un simulador de "tiempo de juego" 
 * que incrementa artificialmente las horas jugadas y desbloquea logros en tiempo real.
 */

import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-library',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './library.html',
  styleUrl: './library.css'
})
export class LibraryComponent implements OnInit, OnDestroy {
  // ==========================================
  // VARIABLES DE ESTADO Y DATOS
  // ==========================================
  myGames: any[] = [];         // Arreglo que contiene todos los juegos comprados por el usuario
  selectedGame: any = null;    // El juego que actualmente está enfocado en el panel principal
  username: string = '';

  // ==========================================
  // VARIABLES DEL TEMPORIZADOR (SIMULADOR DE JUEGO)
  // ==========================================
  isPlaying: boolean = false;
  playTimer: any;              // Almacena la referencia al intervalo (reloj) para poder detenerlo después
  secondsPlaying: number = 0;  // Contador de segundos reales transcurridos en la sesión actual

  // Inyectamos ChangeDetectorRef para forzar la actualización de la interfaz durante el temporizador
  constructor(private cdr: ChangeDetectorRef) {}

  // ==========================================
  // CICLO DE VIDA DEL COMPONENTE
  // ==========================================
  
  /**
   * ngOnInit: Se ejecuta al abrir la biblioteca.
   * Recupera el nombre de usuario de la sesión y carga su lista de juegos.
   */
  ngOnInit(): void {
    this.username = localStorage.getItem('nexus_username') || '';
    this.loadLibrary();
  }

  /**
   * ngOnDestroy: Se ejecuta justo antes de que Angular destruya el componente 
   * (por ejemplo, si el usuario hace clic en "Tienda" o "Perfil" mientras está jugando).
   * Actúa como un mecanismo de seguridad para detener el temporizador y guardar el progreso.
   */
  ngOnDestroy(): void {
    if (this.isPlaying) {
      this.stopPlaying();
    }
  }

  // ==========================================
  // MÉTODOS DE GESTIÓN DE LA BIBLIOTECA
  // ==========================================
  
  /**
   * Lee el LocalStorage buscando la clave específica del usuario activo 
   * y carga sus juegos. Si tiene juegos, auto-selecciona el primero de la lista.
   */
  loadLibrary(): void {
    if (!this.username) return;
    const libraryKey = `nexus_library_${this.username}`;
    this.myGames = JSON.parse(localStorage.getItem(libraryKey) || '[]');
    
    // Seleccionar automáticamente el primer juego si hay alguno
    if (this.myGames.length > 0) {
      this.selectedGame = this.myGames[0];
    }
  }

  /**
   * Cambia el juego activo en el panel principal.
   * Bloquea el cambio si hay una sesión de juego en curso para evitar pérdida de datos.
   */
  selectGame(game: any): void {
    // Evitamos cambiar de juego si hay uno ejecutándose
    if (this.isPlaying) {
      alert('Debes detener el juego actual antes de abrir otro.');
      return;
    }
    this.selectedGame = game;
  }

  // ==========================================
  // LÓGICA DEL SIMULADOR DE JUEGO
  // ==========================================
  
  /**
   * Inicia el temporizador que simula estar jugando.
   * Acelera el tiempo de juego artificialmente para demostraciones académicas.
   */
  playGame(): void {
    if (!this.selectedGame) return;
    this.isPlaying = true;
    this.secondsPlaying = 0;

    // Iniciamos un reloj que se ejecuta repetidamente cada 1000 milisegundos (1 segundo real)
    this.playTimer = setInterval(() => {
      this.secondsPlaying++;
      
      // Lógica acelerada: 1 segundo en la vida real suma 1 minuto (1/60 de hora) en el juego
      this.selectedGame.hoursPlayed += (1 / 60);

      // Sistema de progresión: Cada 20 segundos reales se desbloquea 1 logro automáticamente
      if (this.secondsPlaying % 20 === 0) {
        if (this.selectedGame.achievementsUnlocked < this.selectedGame.totalAchievements) {
          this.selectedGame.achievementsUnlocked += 1;
        }
      }
      
      // Forzamos la actualización visual para ver los números de tiempo y logros subir en vivo
      this.cdr.detectChanges(); 
    }, 1000);
  }

  /**
   * Detiene el intervalo, registra la fecha actual como la última sesión, 
   * y guarda permanentemente los avances en el navegador.
   */
  stopPlaying(): void {
    this.isPlaying = false;
    clearInterval(this.playTimer); // Detenemos el reloj en memoria
    
    // Actualizamos la fecha de última sesión con formato "Día MES" (Ej. "25 OCT")
    const today = new Date();
    const months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'];
    this.selectedGame.lastPlayed = `${today.getDate()} ${months[today.getMonth()]}`;

    this.saveLibrary(); // Guardamos los avances en el navegador
  }

  /**
   * Busca el juego modificado dentro del arreglo y actualiza el LocalStorage.
   */
  saveLibrary(): void {
    const libraryKey = `nexus_library_${this.username}`;
    const index = this.myGames.findIndex(g => g.id === this.selectedGame.id);
    
    if (index !== -1) {
      this.myGames[index] = this.selectedGame;
      localStorage.setItem(libraryKey, JSON.stringify(this.myGames));
    }
  }

  /**
   * Calcula el porcentaje de logros obtenidos matemáticamente.
   * Utilizado en la vista (HTML) para determinar el ancho de la barra de progreso roja.
   */
  getAchievementPercentage(game: any): number {
    if (!game || game.totalAchievements === 0) return 0;
    return (game.achievementsUnlocked / game.totalAchievements) * 100;
  }
}