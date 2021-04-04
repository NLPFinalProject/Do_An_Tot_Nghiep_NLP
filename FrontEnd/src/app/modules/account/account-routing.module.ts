import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';

import { AccountComponent } from './account.component';

const routes: Routes = [
  {
    path: '',
    component: AccountComponent,
    data: {
      title: extract('Thông tin tài khoản'),
      urls: [{ title: 'Trang chính', url: '/' }, { title: 'Thông tin tài khoản' }]
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: []
})
export class AccountRoutingModule {}
