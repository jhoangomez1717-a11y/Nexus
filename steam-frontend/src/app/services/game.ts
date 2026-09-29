/**
 * Archivo: game.ts (GameService)
 * Propósito: Servicio centralizado para la comunicación HTTP con la API REST de Django.
 * Se encarga de realizar todas las peticiones (GET, POST) relacionadas con el catálogo 
 * de juegos y las interacciones de la comunidad (reseñas).
 * Está decorado con @Injectable({ providedIn: 'root' }), lo que significa que Angular 
 * crea una única instancia (Singleton) de este servicio disponible en toda la aplicación.
 */

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class GameService {
  
  // URL base de nuestro backend en Django donde expusimos los endpoints de la API
  private apiUrl = 'http://127.0.0.1:8000/api/games/';

  // Inyectamos HttpClient en el constructor para poder hacer peticiones a la red
  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista del catálogo de juegos.
   * @param url - Opcional. Permite recibir una URL específica (ej. para paginación o búsqueda).
   * Si no se recibe una URL, utiliza la apiUrl por defecto.
   * Retorna un Observable al que los componentes se pueden suscribir para recibir los datos asíncronos.
   */
  getGames(url?: string): Observable<any> {
    return this.http.get<any>(url || this.apiUrl);
  }

  /**
   * Obtiene las reseñas asociadas a un juego específico.
   * @param gameId - El ID numérico del juego en la base de datos.
   * Llama al endpoint de Django que, si no hay reseñas locales, hace Web Scraping a Steam.
   */
  getReviews(gameId: number): Observable<any> {
    return this.http.get<any>(`http://127.0.0.1:8000/api/reviews/?game=${gameId}`);
  }

  /**
   * Envía una nueva reseña escrita por el usuario hacia la base de datos.
   * @param reviewData - Un objeto JSON que contiene la calificación, comentario y el ID del juego.
   * Utiliza el método POST para insertar el registro en Django.
   */
  postReview(reviewData: any): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:8000/api/reviews/', reviewData);
  }
}