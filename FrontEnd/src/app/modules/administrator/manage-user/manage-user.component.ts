import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../login/user-authenticate-service';
@Component({
  selector: 'app-manage-user',
  templateUrl: './manage-user.component.html',
  styleUrls: ['./manage-user.component.scss'],
})
export class ManageUserComponent implements OnInit {
  constructor(private userService: UserService) {}
  //public users:Array<Object>;
  ngOnInit(): void {}
}
