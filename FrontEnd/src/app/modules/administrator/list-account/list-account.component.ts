import { Component, Injector, OnInit } from '@angular/core';
import { AppComponentBase } from '@app/core';

import { ListAccountService } from './utils/services/list-account.service';

@Component({
  selector: 'app-list-account',
  templateUrl: './list-account.component.html',
  styleUrls: ['./list-account.component.scss']
})
export class ListAccountComponent extends AppComponentBase implements OnInit {
  users: Array<object> = [];

  sortName: any = null;
  sortValue: any = null;
  constructor(private injector: Injector, private listAccountService: ListAccountService) {
    super(injector);
  }

  ngOnInit() {
    this.getUsers();
  }

  getUsers(): void {
    this.listAccountService.getJSON().subscribe((res: any) => {
      this.users = res;
      console.log('users', this.users);
    });
  }

  sort(sortName: string, value: boolean): void {
    this.sortName = sortName;
    this.sortValue = value;
    // tslint:disable-next-line:forin
    // for (const key in this.sortMap) {
    //   this.sortMap[key] = key === sortName ? value : null;
    // }
    this.search();
  }

  search(value?: string): void {
    const data = this.users.filter((x: any) => x.name === value);
    this.users = data.sort((a: any, b: any) =>
      this.sortValue === 'ascend'
        ? a[this.sortName] > b[this.sortName]
          ? 1
          : -1
        : b[this.sortName] > a[this.sortName]
        ? 1
        : -1
    );
  }
}
