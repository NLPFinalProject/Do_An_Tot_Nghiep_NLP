import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { NgZorroAntdModule } from 'ng-zorro-antd';

import { DaoVanControlComponent, DaoVanDetailComponent } from '.';
import { DaoVanRoutingModule } from './dao-van-routing.module';
import { DaoVanComponent } from './dao-van.component';
import { ListFileSuccessComponent } from './component/list-file-success/list-file-success.component';
import { DiffContentComponent } from './component/diff-content/diff-content.component';
import { SectionDiffComponent } from './component/section-diff/section-diff.component';
import { ListFileDiffComponent } from './component/list-file-diff/list-file-diff.component';

const COMPONENT = [DaoVanControlComponent, DaoVanDetailComponent, DaoVanComponent];
const MODULE = [CommonModule, DaoVanRoutingModule, NgZorroAntdModule, SharedModule];
@NgModule({
  declarations: [
    ...COMPONENT,
    ListFileSuccessComponent,
    DiffContentComponent,
    SectionDiffComponent,
    ListFileDiffComponent
  ],
  imports: [...MODULE],
  exports: [...COMPONENT]
})
export class DaoVanModule {}
