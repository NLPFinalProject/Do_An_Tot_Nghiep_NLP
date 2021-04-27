import { Component, Injector, OnInit, Input } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AppComponentBase, AuthenticationService, I18nService, Logger, Credentials } from '@app/core';
import { MessageError } from '@app/core/common/errorMessage';
import { CommonConstant, MessageConstant } from '@app/shared';
import { RoutingConstant } from '@app/shared/commons/routing.constant';
import { environment } from '@env/environment';
import { finalize } from 'rxjs/operators';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
@Component({
  selector: 'app-validation',
  templateUrl: './validation.component.html',
  styleUrls: ['./validation.component.scss'],
})
export class ValidationComponent extends AppComponentBase implements OnInit {
  version: string = environment.version;
  error: string;
  validateForm: FormGroup;
  isLoading = false;
  loading = false;
  errors = MessageError.Errors;
  textErrors = MessageError.TextError;
  optionAccounts = CommonConstant.OptionAccounts;
  statusAccount = true;
  isError = false;
  userinfo = {};
  validCode: string;

  constructor(
    injector: Injector,
    private router: Router,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private i18nService: I18nService,
    private authenticationService: AuthenticationService,
    private UserService: UserService
  ) {
    super(injector);
    this.createForm();
    this.loading = true;

    if (this.router.getCurrentNavigation().extras.state != undefined) {
      console.log(this.router.getCurrentNavigation());
      if (this.router.getCurrentNavigation().extras.state.active.validCode != null) {
        this.validCode = this.router.getCurrentNavigation().extras.state.active.validCode;
        this.userinfo = this.router.getCurrentNavigation().extras.state.active.data;
      } else this.validCode = null;
      console.log(this.validCode);
      this.loading = true;
    } else {
      console.log(this.router.getCurrentNavigation().extras.state != undefined);
      this.router.navigate(['login'], { replaceUrl: true });
    }
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }

  ngOnInit() {}

  optionAccount(value: boolean): void {
    this.optionAccounts = value === true ? 'Client' : 'Administator';
    this.statusAccount = value;
  }

  validate() {
    if (this.userinfo == null) {
      console.log('there is nothing we can do');
    } else {
      console.log(data);
      console.log(this.validateForm.value.username);
      console.log(this.validateForm);
      var data = {
        valicode: this.validCode,
        userinfo: this.userinfo,
        confirmpassword: this.validateForm.value.username,
      };
      //data = this.userinfo;

      this.UserService.ActivateUser(data).subscribe(
        //data=> {console.log(data)};
        (data: any) => {
          console.log('we success');
          console.log(data);
          //this.notificationService.success(MessageConstant.RegisterSucssec);
          setTimeout(() => {
            //this.router.navigate(['validate'], { replaceUrl: true })
            this.router.navigate(['login'], { replaceUrl: true });
          }, 1000);
          //this.notificationService.warning(MessageConstant.LoginFailed);
        },
        (error) => {
          this.notificationService.error('Bạn đa nhập sai mã xác thực, vui lòng thử lại');
        }
      );
    }
  }

  //#endregion

  private createForm() {
    this.validateForm = this.formBuilder.group({
      username: [null, Validators.required],
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
