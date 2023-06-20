import { NgModule } from '@angular/core';
import { MessageService } from 'primeng/api';

import { ChartModule } from 'primeng/chart';
import { ToastModule } from 'primeng/toast';

@NgModule({
  declarations: [],
  exports:[
    ChartModule,
    ToastModule
  ], providers: [
    MessageService
  ]
})
export class PrimeModule { }
