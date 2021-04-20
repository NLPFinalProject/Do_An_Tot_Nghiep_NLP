import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';
import { PageBlogIndexComponent, PageBlogDetailComponent } from '.';

const routes: Routes = [
  { path: '', redirectTo: 'index', pathMatch: 'full' },
  {
    path: 'index',
    component: PageBlogIndexComponent,
  },
  {
    path: 'blog/:id',
    component: PageBlogDetailComponent,
    data: {
      title: extract('Detail'),
      urls: [{ title: 'Blog', url: '/blog' }, { title: 'Detail' }],
    },
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class BlogsRoutingModule {}
