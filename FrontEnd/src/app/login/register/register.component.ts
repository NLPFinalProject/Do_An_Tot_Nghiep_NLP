import { Component, OnInit, Injector } from '@angular/core';
import { MessageError } from '@app/core/common/errorMessage';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { AppComponentBase, I18nService } from '@app/core';
import { Router, ActivatedRoute } from '@angular/router';
import { MessageConstant } from '@app/shared';
import { HttpClient } from '@angular/common/http';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent extends AppComponentBase implements OnInit {
  errors = MessageError.Errors;
  registerForm: FormGroup;
  passwordVisible = false;
  checkPasswordVisible = false;
  isLoading = true;
  dateFormat = 'dd/MM/yyyy';

  constructor(
    injector: Injector,
    private router: Router,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private i18nService: I18nService,
    private UserService: UserService
  ) {
    super(injector);
  }

  //#region Confirm
  updateConfirmValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() => this.registerForm.controls.checkPassword.updateValueAndValidity());
  }

  confirmationValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (control.value !== this.registerForm.controls.password.value) {
      return { confirm: true, error: true };
    }
    return {};
  };

  //#endregion

  ngOnInit() {
    this.createdFrom();
    setTimeout(() => {
      this.isLoading = false;
    }, 1000);
  }

  getCaptcha(e: MouseEvent): void {
    e.preventDefault();
  }

  submitForm(): void {
    console.log(this.registerForm.controls);
    console.log(this.registerForm.controls.email.value);
    //console.log(this.registerForm.controls.username.value);
    console.log(this.registerForm.controls.password.value);

    for (const i in this.registerForm.controls) {
      this.registerForm.controls[i].markAsDirty();
      this.registerForm.controls[i].updateValueAndValidity();
    }

    if (this.registerForm.controls.password.value.length < 6)
      this.notificationService.warning('Mật khẩu không được ít hơn 6 sử cái');
    else {
      // this here will send email
      var data = {
        email: this.registerForm.controls.email.value,
        emailOrganization: this.registerForm.controls.emailOrganization.value,
        organization: this.registerForm.controls.organization.value,
        address: this.registerForm.controls.address.value,
        phoneOrganization: this.registerForm.controls.phoneOrganization.value,

        fullName: this.registerForm.controls.fullName.value,
        //userId: this.registerForm.controls.userId.value,
        password: this.registerForm.controls.password.value,

        phoneNumber: this.registerForm.controls.phoneNumber.value,

        ngaySinh: this.registerForm.controls.ngaySinh.value,
        gioiTinh: this.registerForm.controls.gioiTinh.value,
        //captcha: [null, [Validators.required]],
      };

      console.log(data);
      this.UserService.register(data).subscribe(
        //data=> {console.log(data)};
        (data: any) => {
          console.log('we success');
          if (data.data != 'username is existed') {
          }
          console.log(data);
          this.notificationService.success(MessageConstant.RegisterSucssec);
          setTimeout(() => {
            //this.router.navigate(['validate'], { replaceUrl: true })
            this.router.navigate(['validate'], { replaceUrl: true, state: { active: data } });
          }, 1000);
          //this.notificationService.warning(MessageConstant.LoginFailed);
        },
        (error) => {
          this.notificationService.error('Tài khoản đã bị được sử dụng');
        }
      );
    }
  }

  createdFrom(): void {
    this.registerForm = this.formBuilder.group({
      emailOrganization: [null, [Validators.email]],
      organization: [null],
      address: [null],
      phoneOrganization: [null],
      email: [null, [Validators.email, Validators.required]],
      fullName: [null, [Validators.required]],
      //userId: [null],
      password: [null, [Validators.required]],
      checkPassword: [null, [Validators.required, this.confirmationValidator]],
      phoneNumber: [null, [Validators.required]],
      phoneNumberPrefix: ['+84'],
      ngaySinh: [null, [Validators.required]],
      gioiTinh: [true],
      //captcha: [null, [Validators.required]],
      agree: [false],
    });
  }
}
