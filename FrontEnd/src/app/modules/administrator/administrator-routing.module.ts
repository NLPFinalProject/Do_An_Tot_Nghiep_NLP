import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';

import { AdministratorComponent } from './administrator.component';
import{ManageUserComponent} from './manage-user/manage-user.component'
const routes: Routes = [
  // Module is lazy loaded, see app-routing.module.ts
  { path: '', component: AdministratorComponent, data: { title: extract('Administrator') } },
  { path: 'manage-user', component: ManageUserComponent, data: { title: extract('manage') } },
  { path: 'updatabase', component: ManageUserComponent, data: { title: extract('manage') } },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [],
})
export class AdministratorRoutingModule {}
