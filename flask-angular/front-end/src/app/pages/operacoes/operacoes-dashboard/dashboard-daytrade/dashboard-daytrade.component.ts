import { Component, EventEmitter, Input, OnInit } from '@angular/core';
import { ChartType, ChartConfiguration } from 'chart.js';

import { ParValues } from '../../../../components/panel-result/par-value';

// TODO organizar melhor, o que puder passar para funcao ao invez de variavel, separar cada grafico em componente e passar um object com dados

@Component({
  selector: 'app-dashboard-daytrade',
  templateUrl: './dashboard-daytrade.component.html',
  styleUrls: ['./dashboard-daytrade.component.scss'],
})
export class DashboardDaytradeComponent implements OnInit {

  @Input() onLoad!: EventEmitter<any>;

  public results: ParValues[] = [];
  public lineChartType: ChartType = 'line';

  private lineChartQuarterLabels: string[] = [];
  private lineChartQuarterDataRows: number[] = [];

  private lineChartMonthyLabels: string[] = [];
  private lineChartMonthyDataRows: number[] = [];

  public observacoes: any[] = []


  constructor() { }


  ngOnInit() {
    this.onLoad.subscribe({
      next: (resp: any) => {
        this.setup(resp.data)
      }
    })
  }

  setup(data: any): void {
    const daytrade_operations = data.daytrade_operations
    this.results.push({ label: 'Semana', value: daytrade_operations.total_semanal })
    this.results.push({ label: 'Mês', value: daytrade_operations.total_mensal })
    this.results.push({ label: 'Ano', value: daytrade_operations.total_anual })
    this.results.push({ label: 'Acumulado', value: daytrade_operations.total_acumulado })
    this.observacoes = data.daytrade_operations.observacoes



    for (const item of daytrade_operations.quarterly_grouping) {
      this.lineChartQuarterLabels.push(item.data_group)
      this.lineChartQuarterDataRows.push(item.total)
    }

    for (const item of daytrade_operations.monthly_grouping) {
      this.lineChartMonthyLabels.push(item.data_group)
      this.lineChartMonthyDataRows.push(item.total)
    }
  }


  public lineChartQuarterData(): ChartConfiguration['data'] {
    const data = {
      datasets: [
        {
          data: this.lineChartQuarterDataRows,
          label: 'Evolução de resultados Trimestral',
          backgroundColor: 'rgba(148,159,177,0.2)',
          borderColor: 'rgba(148,159,177,1)',
          pointBackgroundColor: 'red',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(148,159,177,0.8)',
          fill: 'origin',
        }
      ],
      labels: this.lineChartQuarterLabels
    }
    return data
  };


  public lineChartQuarterOptions() {
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


  public lineChartMonthyData(): ChartConfiguration['data'] {
    const data = {
      datasets: [
        {
          data: this.lineChartMonthyDataRows,
          label: 'Evolução de resultados Mensal',
          backgroundColor: 'rgba(148,159,177,0.2)',
          borderColor: 'rgba(148,159,177,1)',
          pointBackgroundColor: 'blue',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(148,159,177,0.8)',
          fill: 'origin',
        }
      ],
      labels: this.lineChartMonthyLabels
    }
    return data
  };

  public lineChartMonthyOptions() {
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
            color: 'rgba(71, 124, 171, 0.459)',
          },
        }
      }

    }
    return lineChartOptions
  }


  
}
