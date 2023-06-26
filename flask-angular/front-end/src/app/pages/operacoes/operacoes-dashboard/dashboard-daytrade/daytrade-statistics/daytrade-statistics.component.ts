import { Component } from '@angular/core';
import { formatCurrency } from '@angular/common';

import { ChartType } from 'chart.js';

import { OperacoesService } from '../../../services/operacoes.service';

interface TradingStats {
  avg_gain: number;
  avg_loss: number;
  avg_total: number;
  biggest_gain: number;
  biggest_loss: number;
  costs_total: number;
  count_gain: number;
  count_loss: number;
  gross_total: number;
  net_total: number;
  perc_gain: number;
  total_trades: number;
}

@Component({
  selector: 'app-daytrade-statistics',
  templateUrl: './daytrade-statistics.component.html',
  styleUrls: ['./daytrade-statistics.component.scss']
})
export class DaytradeStatisticsComponent {





  public periodType = '3';
  public barChartType: ChartType = 'bar';
  public barChartLegend = true;
  public barChartLabels: string[] = [];
  public barChartData: any[] = [];
  public barChartPlugins = [];
  public statistics!: TradingStats;

  private filter = new Map();




  constructor(private service: OperacoesService) {
    this.statistics = {
      avg_gain: 0,
      avg_loss: 0,
      avg_total: 0,
      biggest_gain: 0,
      biggest_loss: 0,
      costs_total: 0,
      count_gain: 0,
      count_loss: 0,
      gross_total: 0,
      net_total: 0,
      perc_gain: 0,
      total_trades: 0
    }

  }

  ngOnInit() {
    this.load()
  }

  private load() {
    this.filter.set('period_type', this.periodType)
    this.service.load_statistics_daytrade(this.filter).subscribe({
      next: (resp) => {
        this.statistics = resp.data.statistics

        const labels_set = new Set();
        const ativos = new Set();
        const items = resp.data.operacoes;
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
        text: 'Total diário',
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


  onSelectPeriodType(type: any): void {
    this.periodType = type
    this.load()
  }


}
