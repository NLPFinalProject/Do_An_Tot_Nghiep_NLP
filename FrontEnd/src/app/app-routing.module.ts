import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { Shell } from '@app/shell/shell.service';

const routes: Routes = [
  Shell.childRoutes([
    { path: '', loadChildren: () => import('app/modules/dao-van/dao-van.module').then((m) => m.DaoVanModule) },
  ]),
  Shell.childRoutes([
    { path: 'account', loadChildren: () => import('app/modules/account/account.module').then((m) => m.AccountModule) },
  ]),

  Shell.childRoutes([
    {
      path: 'checkresult',
      loadChildren: () =>
        import('app/modules/validate-result/validate-result.module').then((m) => m.VaildateResultModule),
    },
  ]),
  Shell.childRoutes([
    {
      path: 'admin',
      loadChildren: () => import('app/modules/administrator/administrator.module').then((m) => m.AdministratorModule),
    },
  ]),
  Shell.childRoutes([
    { path: 'about', loadChildren: () => import('app/about/about.module').then((m) => m.AboutModule) },
  ]),

  // Fallback when no prior route is matched
  { path: '**', redirectTo: '', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules, relativeLinkResolution: 'legacy' })],
  exports: [RouterModule],
  providers: [],
})
export class AppRoutingModule {}
