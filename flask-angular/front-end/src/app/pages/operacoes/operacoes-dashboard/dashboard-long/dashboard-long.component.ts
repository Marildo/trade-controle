import { Component, EventEmitter, Input } from '@angular/core';
import { ChartType } from 'chart.js';
import { ParValues } from '../panel-result/par-value';

@Component({
  selector: 'app-dashboard-long',
  templateUrl: './dashboard-long.component.html',
  styleUrls: ['./dashboard-long.component.scss']
})
export class DashboardLongComponent {

 


@Input() onLoad!: EventEmitter<any>;

public results: ParValues[] = [];
 


constructor() { }


ngOnInit() {
  this.onLoad.subscribe({
    next: (resp: any) => {
      this.setup(resp.data)
    }
  })
}

setup(data: any): void {
  const daytrade_operations = data.long_operations
  this.results.push({ label: 'Semana', value: daytrade_operations.total_semanal })
  this.results.push({ label: 'Mês', value: daytrade_operations.total_mensal })
  this.results.push({ label: 'Ano', value: daytrade_operations.total_anual })
  this.results.push({ label: 'Acumulado', value: daytrade_operations.total_acumulado })

   
}
}