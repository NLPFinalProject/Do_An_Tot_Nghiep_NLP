import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { RouterModule } from '@angular/router';
import { AccountComponent } from '.';
import { AccountRoutingModule } from './account-routing.module';
import { NzDropDownModule } from 'ng-zorro-antd/dropdown';
import { AuthInterceptor } from '../../core/authentication/authentication.service';
const COMPONENT = [AccountComponent];
const MODULE = [
  CommonModule,
  TranslateModule,
  NgZorroAntdModule,
  AccountRoutingModule,
  SharedModule,
  RouterModule,
  NzDropDownModule,
  //AuthInterceptor
];
@NgModule({
  declarations: [...COMPONENT],
  imports: [...MODULE],
})
export class AccountModule {}
