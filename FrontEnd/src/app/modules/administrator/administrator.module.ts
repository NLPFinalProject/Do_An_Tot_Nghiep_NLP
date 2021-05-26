import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';

import { AdministratorRoutingModule } from './administrator-routing.module';
import { AdministratorComponent } from './administrator.component';
import { ListAccountComponent } from './list-account/list-account.component';
import { ManageUserComponent } from './manage-user/manage-user.component';
import { UploadDatabaseComponent } from './upload-database/upload-database.component';

const MODULE = [
  CommonModule,
  TranslateModule,
  NgZorroAntdModule,
  SharedModule,
  AdministratorRoutingModule,
  ReactiveFormsModule,
];
@NgModule({
  declarations: [AdministratorComponent, ListAccountComponent, ManageUserComponent, UploadDatabaseComponent],
  imports: [...MODULE],
})
export class AdministratorModule {}
