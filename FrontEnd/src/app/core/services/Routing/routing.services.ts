import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class RoutingService {
  constructor(private router: Router) {}

  navigateToLink(data: any): void {
    this.router.navigate([data]);
  }

  navigateToUpdate(data: any, id: any): void {
    this.router.navigate([data + `/${id}`]);
  }
}
