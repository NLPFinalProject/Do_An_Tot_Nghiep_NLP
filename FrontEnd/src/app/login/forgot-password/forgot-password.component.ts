import { Component, OnInit, Injector } from '@angular/core';
import { AppComponentBase, I18nService } from '@app/core';
import { MessageError } from '@app/core/common/errorMessage';
import { FormGroup, FormBuilder, FormControl, Validators, AbstractControl } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { MessageConstant, RoutingConstant } from '@app/shared';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent extends AppComponentBase implements OnInit {
  errors = MessageError.Errors;
  forgotPasswordForm: FormGroup;
  passwordVisible = false;
  checkPasswordVisible = false;
  isSend = false;
  mail: string;
  constructor(
    injector: Injector,
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private UserService: UserService
  ) {
    super(injector);
  }

  ngOnInit() {
    this.createdFrom();
  }

  getCaptcha(e: MouseEvent): void {
    e.preventDefault();
  }

  submitForm(): void {
    var data = {
      username: this.forgotPasswordForm.controls.email.value,
    };

    console.log(data);
    for (const i in this.forgotPasswordForm.controls) {
      this.forgotPasswordForm.controls[i].markAsDirty();
      this.forgotPasswordForm.controls[i].updateValueAndValidity();
    }
    this.UserService.ForgotPassword(data).subscribe(
      (data) => {
        this.notificationService.success('Đã gửi email thành công, vui lòng xác nhận email');
        this.isSend = true;
        setTimeout(() => {
          this.route.queryParams.subscribe((params) =>
            this.router.navigate([params.redirect || RoutingConstant.Base], { replaceUrl: true })
          );
        }, 5000);
      },
      (error) => {
        this.errors = error;
        //this.notificationService.error("Tài khoản hoặc mật khẩu không chính xác");
        this.showErrorNotification(`Có lỗi xảy ra, vui lòng thử lại`);
      }
    );
  }

  createdFrom(): void {
    this.forgotPasswordForm = this.formBuilder.group({
      email: [null, [Validators.required]],
    });
  }
}
