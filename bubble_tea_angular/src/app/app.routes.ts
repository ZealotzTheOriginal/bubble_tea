import { Routes, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './services/auth.service';
import { map, take } from 'rxjs';

// Evitar ingreso a usuarios no registrados
const authGuard = () => {
  const router = inject(Router);
  const authService = inject(AuthService);
  return authService.user$.pipe(
    take(1),
    map(user => !!user || router.createUrlTree(['/login']))
  );
};

// Evitar ingreso a usuarios registrados
const guestGuard = () => {
  const router = inject(Router);
  const authService = inject(AuthService);
  return authService.user$.pipe(
    take(1),
    map(user => !user || router.createUrlTree(['/home']))
  );
};

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full'
    },
    {
        path: 'home',
        loadComponent: () => import('./pages/home/home').then(m => m.Home),
        canActivate: [authGuard],
    },
    {
        path: 'login',
        loadComponent: () => import('./pages/login/login').then(m => m.Login),
        canActivate: [guestGuard],
    },
    {
        path: '**',
        redirectTo: 'home'
    }
];