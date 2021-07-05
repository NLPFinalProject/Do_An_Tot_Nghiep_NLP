import { Component, Injector, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Data, Router } from '@angular/router';
import { AppComponentBase, AuthenticationService, I18nService, Logger, Credentials } from '@app/core';
import { MessageError } from '@app/core/common/errorMessage';
import { CommonConstant, MessageConstant } from '@app/shared';
import { RoutingConstant } from '@app/shared/commons/routing.constant';
import { environment } from '@env/environment';
import { finalize } from 'rxjs/operators';
import { TranslateService } from '@ngx-translate/core';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
import { lang } from 'moment';

const log = new Logger('Login');

@Component({
  selector: 'app-index-login',
  templateUrl: './index-login.component.html',
  styleUrls: ['./index-login.component.scss'],
})
export class IndexLoginComponent extends AppComponentBase implements OnInit {
  version: string = environment.version;
  error: string;
  loginForm: FormGroup;
  isLoading = false;
  loading = false;
  errors = MessageError.Errors;
  textErrors = MessageError.TextError;
  optionAccounts = CommonConstant.OptionAccounts;
  statusAccount = true;
  isError = false;
  constructor(
    injector: Injector,
    private router: Router,
    private formBuilder: FormBuilder,
    private i18nService: I18nService,
    private authenticationService: AuthenticationService,
    private UserService: UserService,
    private translateService: TranslateService
  ) {
    super(injector);

    this.createForm();
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }

  ngOnInit() {
    //to clear login data
    localStorage.clear();
  }

  optionAccount(value: boolean): void {
    this.optionAccounts = value === true ? 'Client' : 'Administator';
    this.statusAccount = value;
  }

  login() {
    this.isLoading = true;
    var data = {
      username: this.loginForm.controls.username.value,
      password: this.loginForm.controls.password.value,
    };
    //this.UserService

    this.authenticationService
      .login(data)

      .subscribe(
        (value: any) => {
          this.isLoading = false;
          this.loading = false;
          this.authenticationService.setSession(value);
          if (value.token != null) {
            this.UserService.isAdmin(this.loginForm.controls.username.value).subscribe(
              (data: any) => {
                if (data.isAdmin == false) {
                  setTimeout(() => {
                    this.router.navigate(['daovan'], { replaceUrl: true, state: { user: value } });
                  }, 1000);
                } else {
                  localStorage.setItem('isAdmin', 'Yes');
                  setTimeout(() => {
                    this.router.navigate(['admin'], { replaceUrl: true, state: { user: value } });
                  }, 1000);
                }
              },
              (error) => {
                this.isLoading = false;

                this.loading = false;
                log.debug(`Login error: ${error}`);
                this.error = error;
                //this.notificationService.error("Tài khoản hoặc mật khẩu không chính xác");
                this.showErrorNotification(`Tài khoản hoặc mật khẩu không chính xác`);
              }
            );
          } else {
            this.notificationService.error(value.toString() + '1');
            this.loading = false;
          }
        },
        (error) => {
          this.isLoading = false;
          log.debug(`Login error: ${error}`);
          this.error = error;
          if (error.error.data) {
            this.showErrorNotification(error.error.data);
            this.loading = false;
          } else {
            log.debug(`Login error: ${error}`);
            this.error = error;

            this.showErrorNotification(`Tài khoản hoặc mật khẩu không chính xác`);
          }
        }
      );
  }
  //#endregion

  private createForm() {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      remember: true,
    });
  }

  //#region  Language
  setLanguage(language: string) {
    //this.i18nService.language = language;
    this.translateService.use('vn');
  }
  setVNLanguage() {
    //this.i18nService.language = language;

    this.translateService.use('vn');
  }
  setENGLanguage() {
    //this.i18nService.language = language;

    this.translateService.use('en');
  }
  get currentLanguage(): string {
    return this.i18nService.language;
  }

  get languages(): string[] {
    return this.i18nService.supportedLanguages;
  }
}
