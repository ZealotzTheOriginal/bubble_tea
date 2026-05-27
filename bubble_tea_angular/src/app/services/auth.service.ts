import { Injectable, inject, Injector, runInInjectionContext } from '@angular/core';
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, user, updateProfile } from '@angular/fire/auth';
import { Router } from '@angular/router';
import { LoginData, RegisterData, User } from '../models/user.model';
import { map, Observable, shareReplay } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private auth = inject(Auth);
  private router = inject(Router);
  private injector = inject(Injector);

  user$: Observable<User | null> = user(this.auth).pipe(
    map(firebaseUser => firebaseUser ? {
      uid: firebaseUser.uid,
      name: firebaseUser.displayName,
      email: firebaseUser.email
    } : null),
    shareReplay(1)
  );

  async register({ name, email, password }: RegisterData) {
    try {
      const credentials = await runInInjectionContext(this.injector, () =>
        createUserWithEmailAndPassword(this.auth, email, password)
      );
      await runInInjectionContext(this.injector, () =>
        updateProfile(credentials.user, { displayName: name })
      );
      this.router.navigate(['/home']);
    } catch (e) {
      console.error('Error in register', e);
      throw e;
    }
  }

  async login({ email, password }: LoginData) {
    try {
      await runInInjectionContext(this.injector, () =>
        signInWithEmailAndPassword(this.auth, email, password)
      );
      this.router.navigate(['/home']);
    } catch (e) {
      console.error('Error in login', e);
      throw e;
    }
  }

  async logout() {
    await runInInjectionContext(this.injector, () => signOut(this.auth));
    this.router.navigate(['/login']);
  }
}