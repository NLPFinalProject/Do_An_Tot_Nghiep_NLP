import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';

import { AboutComponent } from './about.component';

const routes: Routes = [
  // Module is lazy loaded, see app-routing.module.ts
  { path: '', component: AboutComponent, data: { title: extract('About') } },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [],
})
export class AboutRoutingModule {}
