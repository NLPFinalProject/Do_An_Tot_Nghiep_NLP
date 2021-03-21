import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgZorroAntdModule } from 'ng-zorro-antd';

import { ArticlesComponent, ProfileUserComponent, ReportInputFileComponent } from '.';
import { ListInputFileComponent } from './components/manager-file/list-input-file/list-input-file.component';
import { LoaderComponent } from './loader/loader.component';

const ACCOUNT = [ProfileUserComponent, ArticlesComponent];
const MANAGER_FILE = [ListInputFileComponent];
const COMPOENT = [LoaderComponent, ReportInputFileComponent];
const MODULE = [CommonModule, NgZorroAntdModule, ReactiveFormsModule];
@NgModule({
  imports: [...MODULE],
  declarations: [...COMPOENT, ...ACCOUNT, ...MANAGER_FILE],
  exports: [...COMPOENT, ...ACCOUNT, ...MANAGER_FILE]
})
export class SharedModule {}
