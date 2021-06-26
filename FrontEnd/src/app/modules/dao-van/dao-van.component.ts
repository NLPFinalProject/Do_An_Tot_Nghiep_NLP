import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dao-van',
  templateUrl: './dao-van.component.html',
  styleUrls: ['./dao-van.component.scss'],
})
export class DaoVanComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {
    if (localStorage.getItem('isAdmin') != null) {
      this.router.navigate(['admin'], { replaceUrl: true });
    }
  }
}
