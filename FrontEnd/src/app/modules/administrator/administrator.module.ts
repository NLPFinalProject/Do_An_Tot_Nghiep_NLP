import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';

import { AdministratorRoutingModule } from './administrator-routing.module';
import { AdministratorComponent } from './administrator.component';
import { ListAccountComponent } from './list-account/list-account.component';
import { UploadDatabaseComponent } from './upload-database/upload-database.component';
import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';
//import { NgHighlightModule } from 'ngx-text-highlight';
import { NgxFileDropModule } from 'ngx-file-drop';
import { MatRadioModule } from '@angular/material/radio';
import { MatDialogModule } from '@angular/material/dialog';

//import { MaterialModule } from './material.module';

const MODULE = [
  CommonModule,
  TranslateModule,
  NgZorroAntdModule,
  SharedModule,
  AdministratorRoutingModule,
  ReactiveFormsModule,
  NgxFileDropModule,
  MatRadioModule,
  MatDialogModule,
];
@NgModule({
  declarations: [AdministratorComponent, ListAccountComponent, UploadDatabaseComponent],
  imports: [...MODULE],
})
export class AdministratorModule {}
