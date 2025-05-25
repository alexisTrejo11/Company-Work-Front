import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BidComponent } from "./bid/bid.component";
import { Bid, BidStatus } from './bid/bid.model';
import { BidService } from './bid/bid.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, BidComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  constructor(private bidService: BidService) {}

  get activeBids() {
    return this.bidService.getActiveBids();
  }
}
