
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


import { AtivosMainComponent } from './ativos-main/ativos-main.component';
import { AtivosDashboardComponent } from './ativos-dashboard/ativos-dashboard.component';
import { AtivosIbovespaComponent } from './ativos-ibovespa/ativos-ibovespa.component';
import { AtivosIbovespaItemComponent } from './ativos-ibovespa-item/ativos-ibovespa-item.component';



const ativosRouters: Routes = [
  {
    path: 'ativos',
    component: AtivosMainComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: AtivosDashboardComponent },
      { path: 'ibovespa/:id', component: AtivosIbovespaItemComponent },
      { path: 'ibovespa', component: AtivosIbovespaComponent },      
    ]
  }
]


@NgModule({
  imports: [RouterModule.forChild(ativosRouters)],
  exports: [RouterModule]
})
export class AtivosRoutingModule { }






