import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async'; // <-- 1. Importa esto

import { routes } from './app.routes';

const firebaseConfig = {
  apiKey: "AIzaSyB8SODwJWHBktZb8Lo-9iKFUP7wvbnP9Jo",
  authDomain: "project-modules-2026.firebaseapp.com",
  projectId: "project-modules-2026",
  storageBucket: "project-modules-2026.firebasestorage.app",
  messagingSenderId: "265014454696",
  appId: "1:265014454696:web:52f8984819e6c5a82ed59d",
  measurementId: "G-JF73TMT7VW"
};

export const appConfig: ApplicationConfig = {
  providers: [
    // --- Providers de Angular ---
    provideRouter(routes),
    provideBrowserGlobalErrorListeners(),
    provideAnimationsAsync(),

    // --- Providers de Firebase ---
    provideFirebaseApp(() => initializeApp(firebaseConfig)),
    provideAuth(() => getAuth()),

    // --- Providers de API (Híbrido) ---
    provideHttpClient(),
  ]
};