import { Component, Injector, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Data, Router } from '@angular/router';
import { AppComponentBase, AuthenticationService, I18nService, Logger, Credentials } from '@app/core';
import { MessageError } from '@app/core/common/errorMessage';
import { CommonConstant, MessageConstant } from '@app/shared';
import { RoutingConstant } from '@app/shared/commons/routing.constant';
import { environment } from '@env/environment';
import { finalize } from 'rxjs/operators';
import {UserService} from '@../../../src/app/login/user-authenticate-service'
const log = new Logger('Login');

@Component({
  selector: 'app-index-login',
  templateUrl: './index-login.component.html',
  styleUrls: ['./index-login.component.scss']
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
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private i18nService: I18nService,
    private authenticationService: AuthenticationService,
    private UserService:UserService,

  ) {
    super(injector);
    this.createForm();
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }

  ngOnInit() {}

  optionAccount(value: boolean): void {
    this.optionAccounts = value === true ? 'Client' : 'Administator';
    this.statusAccount = value;
  }
/*
  login() {
    this.isLoading = true;
    this.authenticationService
      .login(this.loginForm.value)
      .pipe(
        finalize(() => {
          this.loginForm.markAsPristine();
          
          setTimeout(() => {
            this.isLoading = false;
          }, 1000);
        })
      )
      .subscribe(
        (credentials: Credentials) => {
          console.log("sucess ");
          const rememberValue = this.loginForm.get('remember').value;
          this.authenticationService.setCredentials(credentials, rememberValue);
          const url = this.statusAccount ? RoutingConstant.DaoVan : RoutingConstant.Admin;
          if (credentials) {
            setTimeout(() => {
              this.route.queryParams.subscribe(params =>
                this.router.navigate([params.redirect || url], { replaceUrl: true })
              );
            }, 1000);
          } else {
            this.isError = true;
          }
        },
        error => {
          log.debug(`Login error: ${error}`);
          this.error = error;
          this.showErrorNotification(`${MessageConstant.LoginFailed}`);
        }
      );
  }*/
  login() {
    this.isLoading = true;
    var data = {
      username:this.loginForm.controls.username.value,
      password:this.loginForm.controls.password.value
    }
    this.UserService
      .login(data)
      
      .subscribe( (value:Data )=> {
          console.log("sucess ");
          console.log(data);
          //const rememberValue = this.loginForm.get('remember').value;
          //this.authenticationService.setCredentials(credentials, rememberValue);
          const url = this.statusAccount ? RoutingConstant.DaoVan : RoutingConstant.Admin;
          if (value.username!=null) {
            
            setTimeout(() => {
              
                this.router.navigate(['daovan'], { replaceUrl: true })
              
            }, 1000);
          }
          else{
            this.isLoading = false;
            this.notificationService.error(value.toString());
          }
        }
        )
  }
  //#endregion

  private createForm() {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      remember: true
    });
  }

  //#region  Language
  setLanguage(language: string) {
    this.i18nService.language = language;
  }

  get currentLanguage(): string {
    return this.i18nService.language;
  }

  get languages(): string[] {
    return this.i18nService.supportedLanguages;
  }
}
