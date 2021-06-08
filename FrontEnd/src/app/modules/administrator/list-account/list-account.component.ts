import { Component, Injector, OnInit } from '@angular/core';
import { AppComponentBase } from '@app/core';
import { UserService } from '../../../login/user-authenticate-service';
import { ListAccountService } from './utils/services/list-account.service';

@Component({
  selector: 'app-list-account',
  templateUrl: './list-account.component.html',
  styleUrls: ['./list-account.component.scss'],
})
export class ListAccountComponent extends AppComponentBase implements OnInit {
  users: Array<any> = [];

  sortName: any = null;
  sortValue: any = null;
  constructor(
    private injector: Injector,
    private listAccountService: ListAccountService,
    private userService: UserService
  ) {
    super(injector);
  }

  ngOnInit() {
    console.log("now I'm here");
    if (localStorage.getItem('isAdmin') != null)
      this.userService.getUserList(localStorage.getItem('isAdmin')).subscribe((data: any) => {
        this.users = data.users;
      });
    //this.getUsers();
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
  lockUser(username: string) {
    console.log('lock is working');
    console.log(username);
    for (var i = 0; i < this.users.length; i++) {
      if (this.users[i].username == username) {
        this.userService.lockUser(username).subscribe((data: any) => {
          console.log('my job is done');
          this.users[i].is_lock = true;
        });
        break;
      }
    }
  }
  unlockUser(username: string) {
    for (var i = 0; i < this.users.length; i++) {
      if (this.users[i].username == username) {
        this.userService.unlockUser(username).subscribe((data: any) => {
          console.log(this.users[i].is_lock);
          console.log(this.users[i].username);
          this.users[i].is_lock = false;
          console.log(this.users[i].is_lock);
        });
        break;
      }
    }
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
