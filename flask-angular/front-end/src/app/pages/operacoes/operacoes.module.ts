import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';



import { OperacoesRoutingModule } from './operacoes.routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { OperacoesMainComponent } from './operacoes-main/operacoes-main.component';
import { OperacoesDashboardComponent } from './operacoes-dashboard/operacoes-dashboard.component';
import { OperacoesSummaryComponent } from './operacoes-summary/operacoes-summary.component';
import { OperacoesDetailComponent } from './operacoes-detail/operacoes-detail.component';
import { OperacoesArquivosComponent } from './operacoes-arquivos/operacoes-arquivos.component';
import { DashboardDaytradeComponent } from './operacoes-dashboard/dashboard-daytrade/dashboard-daytrade.component';
import { DaytradeStatisticsComponent } from './operacoes-dashboard/dashboard-daytrade/daytrade-statistics/daytrade-statistics.component';
import { DashboardLongComponent } from './operacoes-dashboard/dashboard-long/dashboard-long.component';


@NgModule({
  declarations: [
    OperacoesMainComponent,
    OperacoesDashboardComponent, 
    OperacoesSummaryComponent,
    OperacoesDetailComponent,
    OperacoesArquivosComponent,
    DashboardDaytradeComponent,
    DaytradeStatisticsComponent,
    DashboardLongComponent
   ],
  imports: [
    CommonModule,
    SharedModule,
    OperacoesRoutingModule,
  ]
})
export class OperacoesModule { }
