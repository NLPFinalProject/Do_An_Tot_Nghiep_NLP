import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';

import { AccountComponent } from '.';
import { AccountRoutingModule } from './account-routing.module';

const COMPONENT = [AccountComponent];
const MODULE = [CommonModule, TranslateModule, NgZorroAntdModule, AccountRoutingModule, SharedModule];
@NgModule({
  declarations: [...COMPONENT],
  imports: [...MODULE]
})
export class AccountModule {}
