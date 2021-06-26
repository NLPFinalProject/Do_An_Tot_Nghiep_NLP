import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-administrator',
  templateUrl: './administrator.component.html',
  styleUrls: ['./administrator.component.scss'],
})
export class AdministratorComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {
    if (localStorage.getItem('isAdmin') == null) {
      this.router.navigate(['login'], { replaceUrl: true });
    }
  }
  gotoManageUser() {
    console.log('F1');
    this.router.navigate(['updatabase'], { replaceUrl: true });
  }
  gotoUploadDatabase() {
    console.log('F2');
    this.router.navigate(['updatabase'], { replaceUrl: true });
  }
}
