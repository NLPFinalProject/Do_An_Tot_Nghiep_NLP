import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { AuthenticationService, I18nService } from '@app/core';
import { UserService } from '@../../../src/app/login/user-authenticate-service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  styles: [
    `
      [nz-menu] {
        width: 240px;
      }
    `,
  ],
})
export class HeaderComponent implements OnInit {
  menuHidden = true;

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService,
    private i18nService: I18nService,
    private fileService: FileService,
    private userService: UserService
  ) {}

  ngOnInit() {}

  toggleMenu() {
    this.menuHidden = !this.menuHidden;
  }

  setLanguage(language: string) {
    this.i18nService.language = language;
  }

  logout() {
    this.authenticationService.logout().subscribe(() => this.router.navigate(['/login'], { replaceUrl: true }));
  }
  test() {
    console.log('here');
    return this.fileService.testform().subscribe((data) => {
      console.log(data);
      this.router.navigate(['result'], { replaceUrl: true, state: { data: data } });
    });
  }
  test2() {
    console.log('here');
    return this.fileService.testform().subscribe((data) => {
      console.log(data);
      this.router.navigate(['fortest'], { replaceUrl: true, state: { data: data } });
    });
  }
  account() {
    console.log('account pass');
    let id = localStorage.getItem('username');
    return this.userService.profile(id).subscribe((data) => {
      console.log(data);
      this.router.navigate(['account'], { replaceUrl: true, state: { data: data } });
    });
  }
  get currentLanguage(): string {
    return this.i18nService.language;
  }

  get languages(): string[] {
    return this.i18nService.supportedLanguages;
  }

  get username(): string | null {
    const credentials = this.authenticationService.credentials;
    return credentials ? credentials : null;
  }
}
