import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';
import { IndexLoginComponent, RegisterComponent, ForgotPasswordComponent } from '.';
import { LoginComponent } from './login.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { ValidationComponent } from './validation/validation.component';

const routes: Routes = [
  {
    path: '',
    component: LoginComponent,
    children: [
      { path: '', redirectTo: 'login', pathMatch: 'full' },
      { path: 'login', component: IndexLoginComponent, data: { title: extract('Login') } },
      { path: 'register', component: RegisterComponent, data: { title: extract('Register') } },
      { path: 'forgot-password', component: ForgotPasswordComponent, data: { title: extract('Forgot Password') } },
      { path: 'reset-password', component: ResetPasswordComponent, data: { title: extract('Reset Password') } },
      { path: 'validate', component: ValidationComponent, data: { title: extract('Validate email code') } },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [],
})
export class LoginRoutingModule {}
