import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BlogsRoutingModule } from './blogs-routing.module';
import { PageBlogIndexComponent, PageBlogDetailComponent } from '.';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { SharedModule } from '@app/shared/shared.module';

const COMPONENT = [PageBlogIndexComponent, PageBlogDetailComponent];
const MODULE = [CommonModule, BlogsRoutingModule, NgZorroAntdModule, SharedModule];

@NgModule({
  declarations: [...COMPONENT],
  imports: [...MODULE],
})
export class BlogsModule {}
