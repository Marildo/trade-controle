import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AtivosMainComponent } from './ativos-main/ativos-main.component';
import { AtivosDashboardComponent } from './ativos-dashboard/ativos-dashboard.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { AtivosRoutingModule } from './ativos.routing.module';
import { AtivosScreeningComponent } from './ativos-screening/ativos-screening.component';
import { AtivosBacktestComponent } from './ativos-backtest/ativos-backtest.component';



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
