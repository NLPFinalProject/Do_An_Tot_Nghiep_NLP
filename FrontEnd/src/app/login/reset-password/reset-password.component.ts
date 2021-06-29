import { Component, OnInit, Injector } from '@angular/core';
import { AppComponentBase } from '@app/core';
import { MessageError } from '@app/core/common/errorMessage';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';
import { MessageConstant, RoutingConstant } from '@app/shared';
import { Router, ActivatedRoute } from '@angular/router';
import { UserService } from '../user-authenticate-service';
import { throwMatDialogContentAlreadyAttachedError } from '@angular/material/dialog';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss'],
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
    private route: ActivatedRoute,
    private userService: UserService
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
    } else if (control.value !== this.resetPasswordForm.controls.checkPassword.value) {
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

  account() {
    let id = localStorage.getItem('username');
    return this.userService.profile(id).subscribe((data) => {
      console.log(data);
      this.router.navigate(['account'], { replaceUrl: true, state: { data: data } });
    });
  }
  submitForm(): void {
    for (const i in this.resetPasswordForm.controls) {
      this.resetPasswordForm.controls[i].markAsDirty();
      this.resetPasswordForm.controls[i].updateValueAndValidity();
    }
    //this.notificationService.error(`Vui lòng kiểm tra Id người dùng `);
    console.log(this.resetPasswordForm);
    if (this.resetPasswordForm.value.password == this.resetPasswordForm.value.checkPassword) {
      this.notificationService.error(`Mật khẩu cũ đã trùng với mật khẩu mới, xin thử lại `);
    } else {
      var data = {
        username: localStorage.getItem('username'),
        password: this.resetPasswordForm.value.password,
        reset: this.resetPasswordForm.value.checkPassword,
      };
      this.userService.ResetPassword(data).subscribe(
        (data: any) => {
          this.notificationService.success(`Đổi mật khẩu thành công' ${MessageConstant.GoToPage} 5 giây`);
          setTimeout(() => {
            this.route.queryParams.subscribe((params) =>
              this.router.navigate([params.redirect || RoutingConstant.Base], { replaceUrl: true })
            );
          }, 5000);
        },
        (error) => {
          this.notificationService.error('Mật khẩu không đúng, vui lòng thử lại');
        }
      );
    }
  }

  createdFrom(): void {
    this.resetPasswordForm = this.formBuilder.group({
      //userId: [null, [Validators.required]],
      password: [null, [Validators.required]],
      checkPassword: [null, [Validators.required]],
      recheckPassword: [null, [Validators.required, this.confirmationValidator]],
    });
  }
}
