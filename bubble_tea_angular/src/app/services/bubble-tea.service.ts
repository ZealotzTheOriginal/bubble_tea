import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { BubbleTea, BubbleTeaResponse } from '../models/bubble-tea';

@Injectable({
  providedIn: 'root'
})
export class BubbleTeaService {
  private http = inject(HttpClient);
  private apiUrl = 'https://bbt-760x.onrender.com/bubbleteas/';

  getBubbleTeas(): Observable<BubbleTea[]> {
    return this.http.get<BubbleTeaResponse>(this.apiUrl).pipe(
      map(response => response.result)
    );
  }
}
