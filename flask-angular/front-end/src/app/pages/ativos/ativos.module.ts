import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AtivosMainComponent } from './ativos-main/ativos-main.component';
import { AtivosDashboardComponent } from './ativos-dashboard/ativos-dashboard.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { AtivosRoutingModule } from './ativos.routing.module';



@NgModule({
  declarations: [
    AtivosMainComponent,
    AtivosDashboardComponent,
  ],
  imports: [
    CommonModule, 
    SharedModule,
    AtivosRoutingModule
  ]
})
export class AtivosModule { }
