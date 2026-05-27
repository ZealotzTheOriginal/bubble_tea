import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface FilterOptions {
  searchTerm: string;
  isVegan: boolean;
  isHot: boolean;
  hasCaffeine: boolean;
}

@Component({
  selector: 'app-filter',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './filter.html',
  styleUrl: './filter.scss'
})
export class FilterComponent {
  filters: FilterOptions = {
    searchTerm: '',
    isVegan: false,
    isHot: false,
    hasCaffeine: false
  };

  @Output() filterChange = new EventEmitter<FilterOptions>();

  onFilterChange() {
    this.filterChange.emit(this.filters);
  }
}
