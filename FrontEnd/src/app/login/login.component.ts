import { Component, Injector, OnInit } from '@angular/core';
import { AppComponentBase, AuthenticationService, I18nService, Logger, Credentials } from '@app/core';
const log = new Logger('Login');

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent extends AppComponentBase implements OnInit {
  isLoading = false;
  loading = false;
  constructor(injector: Injector) {
    super(injector);
  }

  ngOnInit() {}
}
