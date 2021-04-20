import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { NzNotificationModule } from 'ng-zorro-antd/notification';
import { ArticlesComponent, ProfileUserComponent, ReportInputFileComponent } from '.';
import { ListInputFileComponent } from './components/manager-file/list-input-file/list-input-file.component';
import { LoaderComponent } from './loader/loader.component';

import { ErrorComponent } from './components/errors/error/error.component';

const ACCOUNT = [ProfileUserComponent, ArticlesComponent];
const MANAGER_FILE = [ListInputFileComponent];
const COMPOENT = [LoaderComponent, ReportInputFileComponent, ErrorComponent];
const MODULE = [CommonModule, NgZorroAntdModule, ReactiveFormsModule, NzNotificationModule];
@NgModule({
  imports: [...MODULE],
  declarations: [...COMPOENT, ...ACCOUNT, ...MANAGER_FILE, ErrorComponent],
  exports: [...COMPOENT, ...ACCOUNT, ...MANAGER_FILE],
})
export class SharedModule {}
