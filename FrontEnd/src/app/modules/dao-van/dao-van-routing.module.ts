import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';

import { DaoVanComponent } from './dao-van.component';
import { DaoVanControlComponent } from './dao-van-control/dao-van-control.component';
import { DaoVanDetailComponent } from './dao-van-detail/dao-van-detail.component';

const routes: Routes = [
  {
    path: '',
    component: DaoVanComponent,
    children: [
      { path: '', redirectTo: 'daovan', pathMatch: 'full' },
      {
        path: 'daovan',
        component: DaoVanControlComponent,
        data: {
          title: extract('Home'),
          urls: [{ title: 'Home', url: '/' }],
        },
      },
      {
        path: 'daovan/:id',
        component: DaoVanDetailComponent,
        data: {
          title: extract('Detail'),
          urls: [{ title: 'DaoVan', url: '/daovan' }, { title: 'Detail' }],
        },
      },
      // { path: 'control/:id', component: DetailDaoVanComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [],
})
export class DaoVanRoutingModule {}
