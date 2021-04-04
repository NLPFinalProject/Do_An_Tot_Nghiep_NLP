import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import extract from '@app/core/services/I18N/i18n.service';

import { TeststepComponent } from './teststep/teststep.component';
import { ValidateResultComponent } from './validate-result.component';

const routes: Routes = [
  { path: '', redirectTo: 'result', pathMatch: 'full' },
  {
    path: 'result',
    component: ValidateResultComponent
  },
  {
    path: 'step/:id',
    component: TeststepComponent,
    data: {
      title: extract('Detail'),
      urls: [{ title: 'checkresult', url: '/checkresult' }, { title: 'Detail' }]
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ValidateResultRoutingModule {}
