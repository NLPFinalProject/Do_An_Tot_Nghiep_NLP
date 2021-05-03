import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';

import { AdministratorComponent } from './administrator.component';

const routes: Routes = [
  // Module is lazy loaded, see app-routing.module.ts
  { path: '', component: AdministratorComponent, data: { title: extract('Administrator') } },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [],
})
export class AdministratorRoutingModule {}
