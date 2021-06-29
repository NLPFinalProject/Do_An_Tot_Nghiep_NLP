import { Component, Injector, OnInit, Inject } from '@angular/core';
import { AppComponentBase } from '@app/core';
import { UserService } from '../../../login/user-authenticate-service';
import { ListAccountService } from './utils/services/list-account.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
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
    private userService: UserService,
    public dialog: MatDialog
  ) {
    super(injector);
  }

  ngOnInit() {
    if (localStorage.getItem('isAdmin') != null)
      this.userService.getUserList(localStorage.getItem('isAdmin')).subscribe((data: any) => {
        this.users = data.users;
      });
    //this.getUsers();
  }

  getUsers(): void {
    this.listAccountService.getJSON().subscribe((res: any) => {
      this.users = res;
    });
  }

  lockUser(username: string) {
    for (var i = 0; i < this.users.length; i++) {
      if (this.users[i].username == username) {
        this.userService.lockUser(username).subscribe((data: any) => {
          this.users[i].is_lock = true;
        });
        //this.dialog.u
        this.openLockUserDialog(username);
        break;
      }
    }
  }
  openLockUserDialog(username: string) {
    const dialogRef = this.dialog.open(LockUserDialog, {
      width: '250px',
      data: { name: username },
    });
  }
  openUnlockUserDialog(username: string) {
    const dialogRef = this.dialog.open(UnlockUserDialog, {
      width: '250px',
      data: { name: username },
    });
  }
  unlockUser(username: string) {
    for (var i = 0; i < this.users.length; i++) {
      if (this.users[i].username == username) {
        this.userService.unlockUser(username).subscribe((data: any) => {
          this.users[i].is_lock = false;
        });
        this.openUnlockUserDialog(username);
        break;
      }
    }
  }
}
@Component({
  selector: 'lock-user-success-dialog',
  templateUrl: 'lock-user-success-diaglog.html',
})
export class LockUserDialog {
  constructor(
    public dialogRef: MatDialogRef<LockUserDialog>,

    @Inject(MAT_DIALOG_DATA)
    public data: any
  ) {}

  LockUserDialog(): void {
    this.dialogRef.close();
  }
  ConfirmClick(): void {
    this.dialogRef.close();
  }
}

@Component({
  selector: 'unlock-user-success-dialog',
  templateUrl: 'unlock-user-success-dialog.html',
})
export class UnlockUserDialog {
  constructor(
    public dialogRef: MatDialogRef<UnlockUserDialog>,

    @Inject(MAT_DIALOG_DATA)
    public data: any
  ) {}

  UnlockUserDialog(): void {
    this.dialogRef.close();
  }
  ConfirmClick(): void {
    this.dialogRef.close();
  }
}
