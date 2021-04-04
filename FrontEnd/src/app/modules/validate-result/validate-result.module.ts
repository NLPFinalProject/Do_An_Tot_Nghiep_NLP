import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { HttpClientModule } from '@angular/common/http';
import { ValidateResultComponent } from './validate-result.component';
import { TeststepComponent } from './teststep/teststep.component';
import { ValidateResultRoutingModule } from './validate-result.routing.module';
import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';
import { NgHighlightModule } from 'ngx-text-highlight';

const COMPONENT = [ValidateResultComponent, TeststepComponent];
const MODULE = [
  CommonModule,
  TranslateModule,
  ValidateResultRoutingModule,
  NgZorroAntdModule,
  SharedModule,
  ScrollToModule,
  NgHighlightModule,
];
@NgModule({
  declarations: [...COMPONENT],
  imports: [...MODULE]
})
export class VaildateResultModule {}
