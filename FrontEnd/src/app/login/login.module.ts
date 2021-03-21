import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { TranslateModule } from '@ngx-translate/core';
import { NgxErrorsModule } from '@polarcape/ngx-errors';
import { NgZorroAntdModule } from 'ng-zorro-antd';

import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { RegisterComponent } from './register/register.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { IndexLoginComponent } from './index-login/index-login.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { ValidationComponent } from './validation/validation.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TranslateModule,
    NgbModule,
    LoginRoutingModule,
    NgZorroAntdModule,
    NgxErrorsModule
  ],
  declarations: [
    LoginComponent,
    RegisterComponent,
    ForgotPasswordComponent,
    IndexLoginComponent,
    ResetPasswordComponent,
    ValidationComponent
  ]
})
export class LoginModule {}
