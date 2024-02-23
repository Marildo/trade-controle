import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SetupMainComponent } from './setup-main/setup-main.component';
import { SetupDashboardComponent } from './setup-dashboard/setup-dashboard.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { SetupRoutingModule } from './setups.routing.module';
import { SetupScreeningComponent } from './setup-screening/setup-screening.component';
import { SetupBacktestComponent } from './setup-backtest/setup-backtest.component';



@NgModule({
  declarations: [
    SetupMainComponent,
    SetupDashboardComponent,
    SetupBacktestComponent,
    SetupScreeningComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    SetupRoutingModule    
  ]
})
export class SetupsModule { }
