
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


import { AtivosMainComponent } from './ativos-main/ativos-main.component';
import { AtivosDashboardComponent } from './ativos-dashboard/ativos-dashboard.component';
import { AtivosScreeningComponent } from './ativos-screening/ativos-screening.component';
import { AtivosBacktestComponent } from './ativos-backtest/ativos-backtest.component';
 

 


const ativosRouters: Routes = [
  {
    path: 'ativos',
    component: AtivosMainComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: AtivosDashboardComponent },
      { path: 'acoes', component: AtivosDashboardComponent },
      { path: 'screening', component: AtivosScreeningComponent },
      { path: 'backtest', component: AtivosBacktestComponent },
    ]
  }
]


@NgModule({
  imports: [RouterModule.forChild(ativosRouters)],
  exports: [RouterModule]
})
export class AtivosRoutingModule { }






