/**
 * Archivo: game-list.ts
 * Propósito: Controlador (Lógica TypeScript) del componente del catálogo de juegos.
 * Este es el "cerebro" de la tienda. Se encarga de conectarse a la API de Django para 
 * obtener la lista de juegos y sus reseñas, maneja la paginación, el buscador, 
 * y controla el estado de los modales (detalles de juego y pasarela de pago Nequi).
 */

import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; // 👈 IMPORTAMOS EL DETECTOR DE CAMBIOS
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-game-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game-list.html',
  styleUrl: './game-list.css'
})
export class GameListComponent implements OnInit {
  // ==========================================
  // VARIABLES DE ESTADO GLOBALES
  // ==========================================
  games: any[] = [];
  totalGames: number = 0;
  isLoading: boolean = true; // Controla la pantalla de carga (spinner)
  
  // ==========================================
  // VARIABLES DE PAGINACIÓN Y BÚSQUEDA
  // ==========================================
  searchTerm: string = '';
  currentPage: number = 1;
  nextUrl: string | null = null;
  prevUrl: string | null = null;
  currentApiUrl: string = 'http://127.0.0.1:8000/api/games/';

  // ==========================================
  // VARIABLES DEL MODAL DE DETALLES
  // ==========================================
  selectedGame: any = null; // Almacena el juego seleccionado para ver detalles
  gameReviews: any[] = [];
  newReviewComment: string = '';

  // ==========================================
  // VARIABLES DE LA PASARELA DE NEQUI
  // ==========================================
  showNequiModal: boolean = false;
  selectedGameForPurchase: any = null;
  phoneNumber: string = '';
  paymentStatus: string = 'waiting'; // Estados: 'waiting' | 'processing' | 'success'

  // 👇 INYECTAMOS DEPENDENCIAS EN EL CONSTRUCTOR
  constructor(
    private http: HttpClient, 
    public router: Router,
    private cdr: ChangeDetectorRef // Soluciona problemas de renderizado en Angular obligando a redibujar la vista
  ) {}

  /**
   * Método del ciclo de vida de Angular. 
   * Se ejecuta automáticamente justo después de que el componente se carga en memoria.
   */
  ngOnInit(): void {
    this.fetchGames(this.currentApiUrl);
  }

  // ==========================================
  // COMUNICACIÓN CON LA API (BACKEND)
  // ==========================================
  /**
   * Descarga el catálogo de juegos desde Django.
   * @param url - La dirección del endpoint (puede incluir paginación o filtros de búsqueda).
   */
  fetchGames(url: string): void {
    this.isLoading = true;
    this.cdr.detectChanges(); // Forzamos a que salga la animación de carga

    this.http.get(url).subscribe({
      next: (data: any) => {
        // Manejo de la estructura de datos: Si viene con 'results', es paginado.
        if (data.results) {
          this.games = data.results;
          this.totalGames = data.count;
          this.nextUrl = data.next;
          this.prevUrl = data.previous;
        } else {
          // Respaldo por si la API devuelve un arreglo directo
          this.games = data;
          this.totalGames = data.length;
          this.nextUrl = null;
          this.prevUrl = null;
        }
        this.isLoading = false;
        
        // 🪄 MAGIA: Obligamos a Angular a mostrar los juegos inmediatamente sin tener que presionar ninguna tecla
        this.cdr.detectChanges(); 
      },
      error: (err) => {
        console.error('Error cargando juegos', err);
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  // ==========================================
  // MÉTODOS DE BÚSQUEDA Y PAGINACIÓN
  // ==========================================
  onSearch(): void {
    // Construye la URL de búsqueda dinámicamente si el usuario escribió algo
    const url = this.searchTerm 
      ? `http://127.0.0.1:8000/api/games/?search=${this.searchTerm}`
      : 'http://127.0.0.1:8000/api/games/';
    this.currentPage = 1; // Resetea la página al buscar
    this.fetchGames(url);
  }

  nextPage(): void {
    if (this.nextUrl) {
      this.currentPage++;
      this.fetchGames(this.nextUrl);
    }
  }

  prevPage(): void {
    if (this.prevUrl) {
      this.currentPage--;
      this.fetchGames(this.prevUrl);
    }
  }

  // ==========================================
  // LÓGICA DEL MODAL DE DETALLES Y RESEÑAS
  // ==========================================
  /**
   * Abre la ventana modal de un juego específico y descarga sus reseñas.
   */
  openDetails(game: any): void {
    this.selectedGame = game;
    this.gameReviews = [];
    this.newReviewComment = '';
    this.cdr.detectChanges(); // Forzamos abrir el modal visualmente
    
    // 👇 Buscamos tus reseñas de Steam en tu base de datos de Django
    this.http.get(`http://127.0.0.1:8000/api/reviews/?game=${game.id}`).subscribe({
      next: (data: any) => {
        const backendReviews = data.results || data;
        
        // También traemos reseñas nuevas que el usuario haya guardado en el LocalStorage
        const localReviews = JSON.parse(localStorage.getItem('nexus_reviews') || '[]');
        const gameLocalReviews = localReviews.filter((r: any) => r.gameId === game.id);

        // Juntamos todo (Las de Steam de tu DB + las locales nuevas)
        this.gameReviews = [...gameLocalReviews, ...backendReviews];
        
        // 🪄 MAGIA: Obligamos a Angular a pintar las reseñas INMEDIATAMENTE
        this.cdr.detectChanges(); 
      },
      error: (err) => {
        console.error('Error cargando reseñas', err);
        this.cdr.detectChanges();
      }
    });
  }

  closeDetails(): void {
    this.selectedGame = null;
    this.cdr.detectChanges();
  }

  /**
   * Envía una nueva reseña (Simulada en LocalStorage para esta versión).
   */
  submitReview(): void {
    if (!this.newReviewComment.trim()) return; // Evita reseñas vacías
    
    const username = localStorage.getItem('nexus_username');
    if (!username) {
      alert('Debes iniciar sesión para publicar una reseña.');
      this.router.navigate(['/login']);
      return;
    }

    const newReview = {
      gameId: this.selectedGame.id,
      comment: this.newReviewComment,
      author: username
    };

    // Guarda la reseña localmente para que persista
    const localReviews = JSON.parse(localStorage.getItem('nexus_reviews') || '[]');
    localReviews.unshift(newReview); // unshift agrega el elemento al inicio del array
    localStorage.setItem('nexus_reviews', JSON.stringify(localReviews));

    this.gameReviews.unshift(newReview);
    this.newReviewComment = '';
    this.cdr.detectChanges(); // Actualizar las reseñas al instante
    alert('¡Reseña publicada con éxito!');
  }

  // ==========================================
  // LÓGICA DE COMPRA Y PASARELA NEQUI
  // ==========================================
  /**
   * Valida si el usuario está conectado antes de abrir la pasarela de pagos.
   */
  buyGame(game: any): void {
    const username = localStorage.getItem('nexus_username');
    if (!username) {
      this.router.navigate(['/login']); // Redirige al login si es un visitante
      return;
    }
    
    this.selectedGameForPurchase = game;
    this.showNequiModal = true;
    this.paymentStatus = 'waiting';
    this.phoneNumber = '';
    this.cdr.detectChanges();
  }

  /**
   * Simula el proceso de verificación bancaria con un retardo de 3 segundos (setTimeout).
   */
  processPayment(): void {
    if (!this.phoneNumber) return;
    this.paymentStatus = 'processing';
    this.cdr.detectChanges();

    setTimeout(() => {
      this.paymentStatus = 'success';
      this.addGameToLibrary(this.selectedGameForPurchase);
      this.cdr.detectChanges();
    }, 3000);
  }

  /**
   * Añade el juego comprado al inventario personal del usuario en LocalStorage.
   */
  addGameToLibrary(game: any): void {
    const username = localStorage.getItem('nexus_username');
    const libraryKey = `nexus_library_${username}`;
    
    let library = JSON.parse(localStorage.getItem(libraryKey) || '[]');
    
    // Verifica que el usuario no haya comprado el juego antes
    const alreadyOwns = library.find((item: any) => item.id === game.id);
    if (!alreadyOwns) {
      library.push({
        ...game, // Copia todos los atributos originales del juego
        hoursPlayed: 0,
        achievementsUnlocked: 0,
        totalAchievements: 50 // Meta ficticia para simular progresión
      });
      localStorage.setItem(libraryKey, JSON.stringify(library));
    }
  }
}