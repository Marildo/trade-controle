import { Component } from '@angular/core';

import { OperacoesService } from 'src/app/services/operacoes.service';
import { formatCurrency } from '@angular/common';
import { ChartConfiguration, ChartData, ChartEvent, ChartOptions, ChartType} from 'chart.js';



@Component({
  selector: 'app-operacoes-dashboard',
  templateUrl: './operacoes-dashboard.component.html',
  styleUrls: ['./operacoes-dashboard.component.scss']
})
export class OperacoesDashboardComponent {
 


  public barChartType: ChartType = 'bar';
  public barChartLegend = true;
  public barChartLabels: string[] = [];
  public barChartData: any[] = [ ];

  constructor(private service: OperacoesService) {

  }

  ngOnInit() {
      
    this.service.load_dashboard()
      .subscribe({
        next: (resp) => {
          const labels_set = new Set();
          const ativos = new Set();
          const items = resp.data.daytrade_operations.items

          for (const item of items) {
            labels_set.add(item.data)
            ativos.add(item.codigo)
          }

          const datasets = []
          let i = 0
          for (const ativo of ativos) {
            const ops = items.filter((i: any) => i.codigo == ativo)
            const totais = []
            for (const day of labels_set) {
              const value = ops.filter((i: any) => i.data == day)
                .map((i: any) => i.total)[0] || 0
              totais.push(value)
            }

            datasets.push({
              label: ativo,
              data: totais,
              //backgroundColor: "#FFFDD",
            })
            i++
          }
          const labels = Array.from(labels_set)
          this.drawDaytradesChart(labels, datasets)
        },
        error: (e) => {
          console.error(e)
        }
      })


  }

  drawDaytradesChart(labels: any, datasets: any) {
    this.barChartLabels = labels
    this.barChartData = datasets
  }


  public barChartOptions: any = {
    responsive: true,
    scales: {
      x: {
        stacked: true
      },
      y: {
        stacked: true,
        ticks: {
          callback: (value: number) => formatCurrency(value, 'pt-BR','')
        }
      }
    },
    plugins: {
      title: {
        display: true,
        text: 'Resultado diário de daytrade'
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            let label = '';
            if (context.dataset.label) {
              label += `${context.dataset.label}: `;
            }
            if (context.parsed.y !== null) {
              label +=  formatCurrency(context.parsed.y, 'pt-BR', 'R$') 
            }
            return label;
          }
        }
      }
      
    }
    
  };




  public barChartPlugins = [  ];


  
}
