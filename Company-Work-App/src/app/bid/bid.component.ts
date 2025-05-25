import { Component, input, output } from '@angular/core';
import { Bid } from './bid.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-bid',
  imports: [CommonModule],
  templateUrl: './bid.component.html',
  styleUrl: './bid.component.css'
})
export class BidComponent {
  bid = input.required<Bid>();
  allowedToEdit = false;

}
