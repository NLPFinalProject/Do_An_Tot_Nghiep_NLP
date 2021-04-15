import { Component, OnInit, Injector } from '@angular/core';
import { AppComponentBase } from '@app/core';
import { MessageError } from '@app/core/common/errorMessage';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { MessageConstant, RoutingConstant } from '@app/shared';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent extends AppComponentBase implements OnInit {
  errors = MessageError.Errors;
  resetPasswordForm: FormGroup;
  isLoading = true;
  // Check Password
  passwordVisible = false;
  checkPasswordVisible = false;
  constructor(
    injector: Injector,
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute
  ) {
    super(injector);
  }

  //#region Confirm
  updateConfirmValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() => this.resetPasswordForm.controls.checkPassword.updateValueAndValidity());
  }

  confirmationValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (control.value !== this.resetPasswordForm.controls.password.value) {
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
    for (const i in this.resetPasswordForm.controls) {
      this.resetPasswordForm.controls[i].markAsDirty();
      this.resetPasswordForm.controls[i].updateValueAndValidity();
    }
    //this.notificationService.error(`Vui lòng kiểm tra Id người dùng `);
    console.log(this.resetPasswordForm);
    var data = {
      username: localStorage.getItem('username'),
      password: this.resetPasswordForm.value.password,
      reset: '123'
    };

    this.notificationService.success(`${MessageConstant.RegisterSucssec} ${MessageConstant.GoToPage} 5 giây`);
    setTimeout(() => {
      this.route.queryParams.subscribe(params =>
        this.router.navigate([params.redirect || RoutingConstant.Base], { replaceUrl: true })
      );
    }, 5000);
  }

  createdFrom(): void {
    this.resetPasswordForm = this.formBuilder.group({
      //userId: [null, [Validators.required]],
      password: [null, [Validators.required]],
      checkPassword: [null, [Validators.required, this.confirmationValidator]],
      recheckPassword: [null, [Validators.required, this.confirmationValidator]]
    });
  }
}
