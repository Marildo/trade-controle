import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './pages/home/home.component';
import { OperacoesComponent } from './pages/operacoes/operacoes.component';
import { CarteirasComponent } from './pages/carteiras/carteiras.component';

const routes: Routes = [
  // {path:'', component:HomeComponent},
  {path:'', component:OperacoesComponent},
  {path:'operacoes', component:OperacoesComponent},
  {path:'carteiras', component:CarteirasComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
