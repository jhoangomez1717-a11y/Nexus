/**
 * Archivo: auth.ts
 * Propósito: Controlador (Lógica TypeScript) del componente de Autenticación.
 * Maneja el estado del formulario (cambiando entre Login y Registro) y se comunica 
 * con la API de Django para validar credenciales, generar el token de seguridad JWT 
 * o registrar nuevos usuarios en la base de datos.
 */

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Necesario para usar [(ngModel)] en el HTML
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-auth',
  standalone: true,
  // Importamos FormsModule para habilitar la vinculación bidireccional de datos en los inputs
  imports: [CommonModule, FormsModule],
  templateUrl: './auth.html',
  styleUrl: './auth.css'
})
export class AuthComponent {
  // ==========================================
  // VARIABLES DE ESTADO
  // ==========================================
  // Determina qué formulario mostrar. True = Iniciar sesión, False = Registro
  isLoginMode = true; 
  
  // Variables enlazadas directamente a los campos de texto del HTML
  username = '';
  email = '';
  password = '';
  
  // Almacena el mensaje de error si las credenciales fallan o el usuario ya existe
  errorMessage = '';

  // Inyectamos HttpClient para las peticiones a la API y Router para navegación interna
  constructor(private http: HttpClient, private router: Router) {}

  // ==========================================
  // MÉTODOS DE LA INTERFAZ
  // ==========================================
  /**
   * Alterna la interfaz entre el modo de Inicio de Sesión y el modo de Registro.
   * También limpia cualquier mensaje de error previo para no confundir al usuario.
   */
  toggleMode(): void {
    this.isLoginMode = !this.isLoginMode;
    this.errorMessage = '';
  }

  /**
   * Se ejecuta cuando el usuario presiona el botón de "Ingresar" o "Crear cuenta".
   * Evalúa en qué modo se encuentra el formulario y hace la petición correspondiente.
   */
  onSubmit(): void {
    if (this.isLoginMode) {
      // ----------------------------------------
      // 1. FLUJO DE INICIO DE SESIÓN (LOGIN)
      // ----------------------------------------
      // Solicita un token de acceso a la API de Django (JWT)
      this.http.post('http://127.0.0.1:8000/api/token/', {
        username: this.username,
        password: this.password
      }).subscribe({
        next: (res: any) => {
          // Si el login es exitoso, guardamos el token de seguridad y el nombre en el navegador
          localStorage.setItem('nexus_token', res.access);
          localStorage.setItem('nexus_username', this.username);
          alert(`¡Bienvenido de vuelta, ${this.username}!`);
          
          // Recargamos la página y redirigimos a la tienda para que el Navbar se actualice
          window.location.href = '/tienda';
        },
        error: () => {
          // Si Django rechaza las credenciales, mostramos este error
          this.errorMessage = 'Usuario o contraseña incorrectos. Inténtalo de nuevo.';
        }
      });
    } else {
      // ----------------------------------------
      // 2. FLUJO DE CREACIÓN DE CUENTA (REGISTRO)
      // ----------------------------------------
      // Llama a nuestro endpoint personalizado register_user en views.py de Django
      this.http.post('http://127.0.0.1:8000/api/register/', {
        username: this.username,
        email: this.email,
        password: this.password
      }).subscribe({
        next: () => {
          // Si la cuenta se crea correctamente, avisamos al usuario
          alert('¡Cuenta creada con éxito! Iniciando sesión...');
          
          // Cambiamos el modo a Login internamente
          this.isLoginMode = true; 
          
          // RECURSIVIDAD PRÁCTICA: Llamamos automáticamente a esta misma función 
          // para iniciar sesión con los datos que acaba de escribir, 
          // ahorrándole tener que dar clic de nuevo.
          this.onSubmit(); 
        },
        error: (err) => {
          // Capturamos errores específicos del backend (ej. "El usuario ya existe")
          this.errorMessage = err.error?.error || 'Ocurrió un error al crear la cuenta.';
        }
      });
    }
  }
}