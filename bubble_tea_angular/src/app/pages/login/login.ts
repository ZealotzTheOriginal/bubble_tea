import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

function passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
  const password = control.get('password');
  const confirmPassword = control.get('confirmPassword');
  if (password && confirmPassword && password.value !== confirmPassword.value) {
    return { passwordMismatch: true };
  }
  return null;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);

  isLogin = signal(true);
  isLoading = signal(false);
  
  // Toast state
  toastMessage = signal<string | null>(null);
  toastVisible = signal(false);
  private toastTimeout: any;

  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  registerForm = this.fb.group(
    {
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required],
    },
    { validators: passwordMatchValidator }
  );

  toggleMode() {
    this.isLogin.update(v => !v);
    this.hideToast();
    this.loginForm.reset();
    this.registerForm.reset();
  }

  showToast(message: string) {
    this.toastMessage.set(message);
    this.toastVisible.set(true);
    
    if (this.toastTimeout) {
      clearTimeout(this.toastTimeout);
    }
    
    this.toastTimeout = setTimeout(() => {
      this.toastVisible.set(false);
    }, 4000);
  }

  hideToast() {
    this.toastVisible.set(false);
  }

  async onSubmit() {
    if (this.isLogin()) {
      if (this.loginForm.invalid) { this.loginForm.markAllAsTouched(); return; }
      this.isLoading.set(true);
      this.hideToast();
      try {
        await this.authService.login(this.loginForm.value as { email: string; password: string });
      } catch (e: any) {
        this.showToast(this.mapFirebaseError(e?.code));
      } finally {
        this.isLoading.set(false);
      }
    } else {
      if (this.registerForm.invalid) { this.registerForm.markAllAsTouched(); return; }
      this.isLoading.set(true);
      this.hideToast();
      try {
        const { name, email, password } = this.registerForm.value as { name: string; email: string; password: string; confirmPassword: string };
        await this.authService.register({ name, email, password });
      } catch (e: any) {
        this.showToast(this.mapFirebaseError(e?.code));
      } finally {
        this.isLoading.set(false);
      }
    }
  }

  private mapFirebaseError(code: string): string {
    const errors: Record<string, string> = {
      'auth/user-not-found': 'No existe una cuenta con este correo.',
      'auth/wrong-password': 'Contraseña incorrecta.',
      'auth/email-already-in-use': 'Este correo ya está en uso.',
      'auth/invalid-email': 'El correo no es válido.',
      'auth/weak-password': 'La contraseña es demasiado débil.',
      'auth/invalid-credential': 'Credenciales inválidas. Verifica tu correo y contraseña.',
    };
    return errors[code] ?? 'Ocurrió un error. Inténtalo de nuevo.';
  }
}
