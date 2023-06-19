import { Component } from '@angular/core';

import { OperacoesService } from 'src/app/services/operacoes.service';
import { formatCurrency } from '@angular/common';
import { ChartType } from 'chart.js';

import { ParValues } from 'src/app/components/panel-result/par-value';

@Component({
  selector: 'app-dashboard-daytrade',
  templateUrl: './dashboard-daytrade.component.html',
  styleUrls: ['./dashboard-daytrade.component.scss'],
})
export class DashboardDaytradeComponent {
  public results: ParValues[] = [ ];
  public barChartType: ChartType = 'bar';
  public barChartLegend = true;
  public barChartLabels: string[] = [];
  public barChartData: any[] = [];
  public barChartPlugins = [];

  constructor(private service: OperacoesService) {}

  ngOnInit() {
    this.service.load_dashboard().subscribe({
      next: (resp) => {
        const daytrade_operations = resp.data.daytrade_operations
        this.results.push( {label: 'Total da Semana', value: daytrade_operations.total_semanal})
        this.results.push( {label: 'Total do Mês', value: daytrade_operations.total_mensal})       
        this.results.push( {label: 'Total do Ano', value: daytrade_operations.total_anual})
        this.results.push( {label: 'Total Acumulado', value: daytrade_operations.total_acumulado})

        const labels_set = new Set();
        const ativos = new Set();
        const items = daytrade_operations.items;
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
        this.drawDaytradesChart(labels, datasets);
      },
      error: (e) => {
        console.error(e);
      },
    });
  }

  drawDaytradesChart(labels: any, datasets: any) {
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
        ticks: {
          callback: (value: number) => formatCurrency(value, 'pt-BR', ''),
        },
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
}
