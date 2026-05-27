import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { BubbleTeaService } from '../../services/bubble-tea.service';
import { BubbleTea } from '../../models/bubble-tea';
import { FilterComponent, FilterOptions } from '../../shared/filter/filter';
import { BubbleTeaCard } from '../../shared/bubble-tea-card/bubble-tea-card';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FilterComponent, BubbleTeaCard],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home implements OnInit {
  authService = inject(AuthService);
  bubbleTeaService = inject(BubbleTeaService);
  
  user$ = this.authService.user$;
  
  allBubbleTeas = signal<BubbleTea[]>([]);
  filteredBubbleTeas = signal<BubbleTea[]>([]);
  
  isLoading = signal(true);
  
  selectedTea = signal<BubbleTea | null>(null);

  ngOnInit() {
    this.bubbleTeaService.getBubbleTeas().subscribe({
      next: (data) => {
        this.allBubbleTeas.set(data);
        
        // Simular 3 segundos de carga para que se vea la animación
        setTimeout(() => {
          this.filteredBubbleTeas.set([...data]);
          this.isLoading.set(false);
        }, 1000);
      },
      error: (err) => {
        console.error('Error fetching bubble teas', err);
        this.isLoading.set(false);
      }
    });
  }

  onFilterChange(filters: FilterOptions) {
    const filtered = this.allBubbleTeas().filter(tea => {
      const matchSearch = tea.nombre.toLowerCase().includes(filters.searchTerm.toLowerCase()) || 
                          tea.tipo_bubbletea.toLowerCase().includes(filters.searchTerm.toLowerCase());
      
      const matchVegan = !filters.isVegan || tea.es_vegano === 1;
      const matchHot = !filters.isHot || tea.disponible_caliente === 1;
      const matchCaffeine = !filters.hasCaffeine || tea.tiene_cafeina === 1;
      
      return matchSearch && matchVegan && matchHot && matchCaffeine;
    });
    this.filteredBubbleTeas.set(filtered);
  }

  onCardClick(tea: BubbleTea) {
    this.selectedTea.set(tea);
  }

  closeModal() {
    this.selectedTea.set(null);
  }

  getModalImageId() {
    const tea = this.selectedTea();
    return tea ? Math.abs(tea.bubbletea_id || 0) % 8 : 0;
  }

  logout() { this.authService.logout(); }
}
