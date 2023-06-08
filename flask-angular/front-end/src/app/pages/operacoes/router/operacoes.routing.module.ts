
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';



import { OperacoesDashboardComponent } from '../operacoes-dashboard/operacoes-dashboard.component';
import { OperacoesMainComponent } from '../operacoes-main/operacoes-main.component';
import { OperacoesSummaryComponent } from '../operacoes-summary/operacoes-summary.component';
import { OperacoesDetailComponent } from '../operacoes-detail/operacoes-detail.component';


const operacoesRouters: Routes = [
  {
    path: 'operacoes',
    component: OperacoesMainComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: OperacoesDashboardComponent },
      { path: 'resumo', component: OperacoesSummaryComponent },
      { path: 'detalhe', component: OperacoesDetailComponent },
    ]
  }
]


@NgModule({
  imports: [RouterModule.forChild(operacoesRouters)],
  exports: [RouterModule]
})
export class OperacoesRoutingModule { }






