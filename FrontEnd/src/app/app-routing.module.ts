import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { Shell } from '@app/shell/shell.service';

const routes: Routes = [
  Shell.childRoutes([{ path: '', loadChildren: 'app/modules/dao-van/dao-van.module#DaoVanModule' }]),
  Shell.childRoutes([{ path: 'account', loadChildren: 'app/modules/account/account.module#AccountModule' }]),
  Shell.childRoutes([{ path: 'blogs', loadChildren: 'app/modules/blogs/blogs.module#BlogsModule' }]),
  Shell.childRoutes([
    { path: 'checkresult', loadChildren: 'app/modules/validate-result/validate-result.module#VaildateResultModule' }
  ]),
  Shell.childRoutes([
    { path: 'admin', loadChildren: 'app/modules/administrator/administrator.module#AdministratorModule' }
  ]),
  Shell.childRoutes([{ path: 'about', loadChildren: 'app/about/about.module#AboutModule' }]),

  // Fallback when no prior route is matched
  { path: '**', redirectTo: '', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule],
  providers: []
})
export class AppRoutingModule {}
