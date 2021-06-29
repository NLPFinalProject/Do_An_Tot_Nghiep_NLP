import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.scss'],
})
export class AccountComponent implements OnInit {
  searchNameList: any;
  searchAddressList: any;
  userdata2: any;
  filterNameList = [
    { text: 'Joe', value: 'Joe' },
    { text: 'Jim', value: 'Jim' },
  ];
  filterAddressList = [
    { text: 'London', value: 'London' },
    { text: 'Sidney', value: 'Sidney' },
  ];
  sortMap = {
    name: '',
    age: '',
    address: '',
  };
  sortName: string = null;
  sortValue: string = null;

  data = [{}];
  displayData = [...this.data];
  constructor(private router: Router) {
    if (this.router.getCurrentNavigation() != undefined) {
      this.userdata2 = this.router.getCurrentNavigation().extras.state.data;
    } else {
      this.router.navigate(['login'], { replaceUrl: true });
    }
  }
  ngOnInit(): void {}
}
