import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AtivosMainComponent } from '../../pages/ativos/ativos-main/ativos-main.component';
import { AtivosDashboardComponent } from '../../pages/ativos/ativos-dashboard/ativos-dashboard.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { AtivosRoutingModule } from '../../pages/ativos/ativos.routing.module';
import { AtivosScreeningComponent } from '../../pages/ativos/ativos-screening/ativos-screening.component';
import { AtivosBacktestComponent } from '../../pages/ativos/ativos-backtest/ativos-backtest.component';



@NgModule({
  declarations: [
    AtivosMainComponent,
    AtivosDashboardComponent,
    AtivosBacktestComponent,
    AtivosScreeningComponent
  ],
  imports: [
    CommonModule, 
    SharedModule,
    AtivosRoutingModule
  ]
})
export class AtivosModule { }
