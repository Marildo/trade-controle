import { Component } from '@angular/core';
import { ChartType, ChartConfiguration } from 'chart.js';

import { OperacoesService } from 'src/app/pages/operacoes/services/operacoes.service';
import { ParValues } from './panel-result/par-value';  

// TODO organizar melhor, o que puder passar para funcao ao invez de variavel, separar cada grafico em componente e passar um object com dados

@Component({
  selector: 'app-dashboard-daytrade',
  templateUrl: './dashboard-daytrade.component.html',
  styleUrls: ['./dashboard-daytrade.component.scss'],
})
export class DashboardDaytradeComponent {


  public results: ParValues[] = [];
  public lineChartType: ChartType = 'line';
  private lineChartLabels: string[] = [];
  private lineChartDataRows: number[] = [];

  constructor(private service: OperacoesService) { }

  ngOnInit() {
    this.service.load_dashboard().subscribe({
      next: (resp) => {
        const daytrade_operations = resp.data.daytrade_operations
        this.results.push({ label: 'Semana', value: daytrade_operations.total_semanal })
        this.results.push({ label: 'Mês', value: daytrade_operations.total_mensal })
        this.results.push({ label: 'Ano', value: daytrade_operations.total_anual })
        this.results.push({ label: 'Acumulado', value: daytrade_operations.total_acumulado })

        for (const item of daytrade_operations.group_trimestral) {
          this.lineChartLabels.push(item.data_group)
          this.lineChartDataRows.push(item.total)
        }
      },
      error: (e) => {
        console.error(e);
      },
    });
  }



  public lineChartData(): ChartConfiguration['data'] {
    const data = {
      datasets: [
        {
          data: this.lineChartDataRows,
          label: 'Evolução de resultados',
          backgroundColor: 'rgba(148,159,177,0.2)',
          borderColor: 'rgba(148,159,177,1)',
          pointBackgroundColor: 'rgba(148,159,177,1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(148,159,177,0.8)',
          fill: 'origin',
        }
      ],
      labels: this.lineChartLabels
    }
    return data
  };


  public lineChartOptions() {
    const lineChartOptions: ChartConfiguration['options'] = {
      responsive: true,
      elements: {
        line: {
          tension: 0.2
        }
      },
      scales: {
        y: {
          grid: {
            color: 'rgba(255,0,0,0.3)',
          },
        }
      }

    }
    return lineChartOptions
  }

}
