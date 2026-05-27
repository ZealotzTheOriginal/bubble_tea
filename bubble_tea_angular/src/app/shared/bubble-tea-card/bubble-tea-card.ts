import { Component, Input, Output, EventEmitter, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BubbleTea } from '../../models/bubble-tea';

@Component({
  selector: 'app-bubble-tea-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bubble-tea-card.html',
  styleUrl: './bubble-tea-card.scss'
})
export class BubbleTeaCard implements OnInit {
  @Input({ required: true }) bubbleTea!: BubbleTea;
  @Output() cardClick = new EventEmitter<BubbleTea>();
  
  imageId = signal(0);

  ngOnInit() {
    this.imageId.set(Math.abs(this.bubbleTea.bubbletea_id || 0) % 8);
  }

  onCardClick() {
    this.cardClick.emit(this.bubbleTea);
  }
}

