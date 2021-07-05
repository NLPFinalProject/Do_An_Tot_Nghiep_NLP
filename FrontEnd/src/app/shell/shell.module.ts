import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { TranslateModule } from '@ngx-translate/core';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { NzMenuModule } from 'ng-zorro-antd/menu';
import { HeaderComponent } from './header/header.component';
import { ShellComponent } from './shell.component';
import { FooterComponent } from './footer/footer.component';
import { BreadcrumbComponent } from './breadcrumb/breadcrumb.component';
import { NzDropDownModule } from 'ng-zorro-antd/dropdown';

const MODULE = [
  CommonModule,
  TranslateModule,
  NgbModule,
  RouterModule,
  NgZorroAntdModule,
  NzDropDownModule,
  NzMenuModule,
];

const COMPONENT = [HeaderComponent, ShellComponent];
@NgModule({
  imports: [...MODULE],
  declarations: [...COMPONENT, FooterComponent, BreadcrumbComponent],
})
export class ShellModule {}
