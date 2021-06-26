import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { RouterModule } from '@angular/router';
import { DaoVanControlComponent, DaoVanDetailComponent } from '.';
import { DaoVanRoutingModule } from './dao-van-routing.module';
import { DaoVanComponent } from './dao-van.component';
import { ListFileSuccessComponent } from './component/list-file-success/list-file-success.component';
import { DiffContentComponent } from './component/diff-content/diff-content.component';
import { SectionDiffComponent } from './component/section-diff/section-diff.component';
import { ListFileDiffComponent } from './component/list-file-diff/list-file-diff.component';
import { NzDropDownModule } from 'ng-zorro-antd/dropdown';
import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';
import { TranslateModule } from '@ngx-translate/core';
import { DaovanServiceService } from './daovan-service.service';
const COMPONENT = [DaoVanControlComponent, DaoVanDetailComponent, DaoVanComponent];
const MODULE = [
  CommonModule,
  DaoVanRoutingModule,
  NgZorroAntdModule,
  SharedModule,
  RouterModule,
  NzDropDownModule,
  ScrollToModule,
  TranslateModule,
];
@NgModule({
  declarations: [
    ...COMPONENT,
    ListFileSuccessComponent,
    DiffContentComponent,
    SectionDiffComponent,
    ListFileDiffComponent,
  ],
  imports: [...MODULE],
  exports: [...COMPONENT],
  providers: [DaovanServiceService],
})
export class DaoVanModule {}
