import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { NzUploadModule } from 'ng-zorro-antd/upload';
import { ValidateResultComponent } from './validate-result.component';
import { TeststepComponent } from './teststep/teststep.component';
import { ValidateResultRoutingModule } from './validate-result.routing.module';
import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';
//import { NgHighlightModule } from 'ngx-text-highlight';
import { NgxFileDropModule } from 'ngx-file-drop';
import { MatRadioModule } from '@angular/material/radio';
import { MatDialogModule } from '@angular/material/dialog';

//import { MaterialModule } from './material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
//import { BrowserAnimationsModule } from '@angular/platform-browser/animation;

const COMPONENT = [ValidateResultComponent, TeststepComponent];
const MODULE = [
  CommonModule,
  TranslateModule,
  ValidateResultRoutingModule,
  NgZorroAntdModule,
  SharedModule,
  ScrollToModule,
  NzUploadModule,
  NgxFileDropModule,
  MatRadioModule,
  MatDialogModule,
  FormsModule,
  ReactiveFormsModule,
  //NgHighlightModule,
];
@NgModule({
  declarations: [...COMPONENT],
  imports: [...MODULE],
})
export class VaildateResultModule {}
