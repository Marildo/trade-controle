import { Component } from '@angular/core';

import { OperacoesService } from 'src/app/pages/operacoes/services/operacoes.service';
import { formatCurrency } from '@angular/common';
import { ChartType, ChartConfiguration, ChartEvent } from 'chart.js';

import { ParValues } from 'src/app/components/panel-result/par-value';

// TODO organizar melhor, o que puder passar para funcao ao invez de variavel, separar cada grafico em componente e passar um object com dados

@Component({
  selector: 'app-dashboard-daytrade',
  templateUrl: './dashboard-daytrade.component.html',
  styleUrls: ['./dashboard-daytrade.component.scss'],
})
export class DashboardDaytradeComponent {

  // bar chart
  public results: ParValues[] = [];
  public barChartType: ChartType = 'bar';
  public barChartLegend = true;
  public barChartLabels: string[] = [];
  public barChartData: any[] = [];
  public barChartPlugins = [];


  // line chart
  public lineChartType: ChartType = 'line';
  private lineChartLabels: string[] = [];
  private lineChartDataRows: number[] = [];

  constructor(private service: OperacoesService) { }

  ngOnInit() {
    this.service.load_dashboard().subscribe({
      next: (resp) => {
        const daytrade_operations = resp.data.daytrade_operations
        this.results.push({ label: 'Total da Semana', value: daytrade_operations.total_semanal })
        this.results.push({ label: 'Total do Mês', value: daytrade_operations.total_mensal })
        this.results.push({ label: 'Total do Ano', value: daytrade_operations.total_anual })
        this.results.push({ label: 'Total Acumulado', value: daytrade_operations.total_acumulado })

        const labels_set = new Set();
        const ativos = new Set();
        const items = daytrade_operations.operacoes;
        for (const item of items) {
          labels_set.add(item.data);
          ativos.add(item.codigo);
        }

        const datasets = [];
        let i = 0;
        for (const ativo of ativos) {
          const ops = items.filter((i: any) => i.codigo == ativo);
          const totais = [];
          for (const day of labels_set) {
            const value =
              ops
                .filter((i: any) => i.data == day)
                .map((i: any) => i.total)[0] || 0;
            totais.push(value);
          }

          datasets.push({
            label: ativo,
            data: totais,
            //backgroundColor: "#FFFDD",
          });
          i++;
        }
        const labels = Array.from(labels_set);
        this.drawBarChart(labels, datasets);

        for (const item of daytrade_operations.group_trimestral){
          this.lineChartLabels.push(item.data_group)
          this.lineChartDataRows.push(item.total)

        }

        // line chart
      },
      error: (e) => {
        console.error(e);
      },
    });
  }

  drawBarChart(labels: any, datasets: any) {
    this.barChartLabels = labels;
    this.barChartData = datasets;
  }

  public barChartOptions: any = {
    responsive: true,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        // ticks: {
        //   callback: (value: number) => formatCurrency(value, 'pt-BR', ''),
        // },
      },
    },
    plugins: {
      title: {
        display: true,
        text: 'Resultado diário de daytrade',
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            let label = '';
            if (context.dataset.label) {
              label += `${context.dataset.label}: `;
            }
            if (context.parsed.y !== null) {
              label += formatCurrency(context.parsed.y, 'pt-BR', 'R$');
            }
            return label;
          },
        },
      },
    },
  };


  public lineChartData(): ChartConfiguration['data']  {
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
      labels:this.lineChartLabels
    }
    return data
  };


  public lineChartOptions() {
    const lineChartOptions: ChartConfiguration['options'] = {
      elements: {
        line: {
          tension: 0.5
        }
      },
      scales: {
        // We use this empty structure as a placeholder for dynamic theming.
        y:
        {
          position: 'left',
        },
        y1: {
          position: 'right',
          grid: {
            color: 'rgba(255,0,0,0.3)',
          },
          ticks: {
            color: 'gray'
          }
        }
      },

      plugins: {
        legend: { display: true },

      }
    };

    return lineChartOptions
  }

}
