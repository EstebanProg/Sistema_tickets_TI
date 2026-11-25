import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  imports: [FormsModule, RouterLink],
  selector: 'app-login',
  styleUrl: './login.css',
  templateUrl: './login.html',
})
export class Login {
  private auth = inject(AuthService);

  email = '';
  password = '';
  loading = signal(false);
  error = signal('');

  submit() {
    this.loading.set(true);
    this.error.set('');
    this.auth.login(this.email, this.password).subscribe({
      next: (r) => {
        console.log('Respuesta del login:', r); // TEMPORAL: en la iteración 10 se guarda la sesión
        this.loading.set(false);
      },
      error: (e) => {
        this.error.set(
          e.status === 401
            ? 'Credenciales incorrectas'
            : e.status === 0
              ? 'No se pudo conectar con el servidor'
              : 'Revisa el email y la contraseña',
        );
        this.loading.set(false);
      },
    });
  }
}