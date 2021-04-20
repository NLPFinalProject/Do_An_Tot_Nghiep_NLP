import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { AuthenticationService, I18nService } from '@app/core';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  constructor(
    private router: Router,
    private authenticationService: AuthenticationService,
    private i18nService: I18nService,
    private fileService: FileService,
    private userService: UserService
  ) {}

  ngOnInit() {}
  account() {
    console.log('account pass');
    let id = localStorage.getItem('username');
    return this.userService.profile(id).subscribe(data => {
      console.log(data);
      this.router.navigate(['account'], { replaceUrl: true, state: { data: data } });
    });
  }
}
