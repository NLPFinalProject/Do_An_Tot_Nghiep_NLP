import { Component, OnInit, Injector } from '@angular/core';
import { MessageError } from '@app/core/common/errorMessage';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { AppComponentBase, I18nService } from '@app/core';
import { Router, ActivatedRoute } from '@angular/router';
import { MessageConstant } from '@app/shared';
import { HttpClient } from '@angular/common/http';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
import { DatePickerService } from 'ng-zorro-antd/date-picker/date-picker.service';
import { now } from 'lodash';
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
  updatePhoneValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() => this.registerForm.controls.phoneNumber.updateValueAndValidity());
  }

  confirmationValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (control.value !== this.registerForm.controls.password.value) {
      return { confirm: true, error: true };
    }
    return {};
  };
  PhoneNumberValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (!this.checkValidPhoneNumber(control.value)) {
      return { confirm: true, error: true };
    }

    return {};
  };
  DateOfBirthValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (!this.checkValidBirthDate(control.value)) {
      return { confirm: true, error: true };
    }

    return {};
  };
  SpecialCharacterValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { error: true, required: true };
    } else if (this.checkSpecialCharacter(control.value)) {
      return { confirm: true };
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

  submitForm(): void {
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
        fullName: this.registerForm.controls.fullName.value,
        password: this.registerForm.controls.password.value,
        phoneNumber: this.registerForm.controls.phoneNumber.value,
        ngaySinh: this.registerForm.controls.ngaySinh.value,
        gioiTinh: this.registerForm.controls.gioiTinh.value,
      };

      this.UserService.register(data).subscribe(
        (data: any) => {
          this.notificationService.success(MessageConstant.RegisterSucssec);
          setTimeout(() => {
            this.router.navigate(['validate'], { replaceUrl: true, state: { active: data } });
          }, 1000);
        },
        (error) => {
          this.notificationService.error('Tài khoản đã được sử dụng');
        }
      );
    }
  }
  checkSpecialCharacter(str: string) {
    var format = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

    if (format.test(str)) {
      return true;
    } else {
      return false;
    }
  }
  checkValidEmail(str: string) {
    var format = /[ `!#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/;

    if (format.test(str)) {
      return true;
    } else {
      return false;
    }
  }
  checkValidPhoneNumber(str: string) {
    let isnum = /^\d+$/.test(str);

    if (isnum) {
      if (str.length < 9 || str.length > 12) {
        return false;
      }
      return true;
    }
  }
  checkValidBirthDate(date: string) {
    var currentDate = new Date();
    var checkDate = new Date(date);
    if (currentDate < checkDate) {
      return false;
    } else {
      return true;
    }
  }

  createdFrom(): void {
    this.registerForm = this.formBuilder.group({
      emailOrganization: [null, [Validators.email]],
      email: [null, [Validators.email, Validators.required]],
      fullName: [null, [Validators.required, Validators.maxLength(32), this.SpecialCharacterValidator]],
      //userId: [null],
      password: [null, [Validators.required]],
      checkPassword: [null, [Validators.required, this.confirmationValidator]],
      phoneNumber: [
        null,
        [Validators.required, Validators.pattern('^[0-9]*$'), Validators.minLength(9), Validators.maxLength(12)],
      ],
      //phoneNumber: [null, [Validators.required,,Validators.pattern("^[0-9]*$")]],
      phoneNumberPrefix: ['+84'],
      ngaySinh: [null, [Validators.required, this.DateOfBirthValidator]],
      gioiTinh: [true],
      //captcha: [false, [Validators.required]],
      agree: [false, [Validators.required]],
    });
  }
}
