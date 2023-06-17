import { Component } from '@angular/core';

@Component({
  selector: 'app-operacoes-dashboard',
  templateUrl: './operacoes-dashboard.component.html',
  styleUrls: ['./operacoes-dashboard.component.scss']
})
export class OperacoesDashboardComponent {
  data: any;

  options: any;

  constructor(private service: OperacoesService) {

  }

  ngOnInit() {
    const documentStyle = getComputedStyle(document.documentElement);
    const colors = [documentStyle.getPropertyValue('--green-100'), documentStyle.getPropertyValue('--blue-800'),]

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
              type: 'bar',
              label: ativo,
              backgroundColor: colors[i],
              data: totais
            })
            i++
          }
          const labels = Array.from(labels_set)
          this.drawChart(labels, datasets)
        },
        error: (e) => {
          console.error(e)
        }
      })


  }

  drawChart(labels: any, datasets: any) {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    this.data = {
      labels,
      datasets
    };

    this.options = {
      title: {
        display: true,
        text: 'Receitas x Despesas'
      },
      maintainAspectRatio: false,
      aspectRatio: 0.8,
      tooltips: {
        callbacks: {
          label: (tooltipItem: any, data: any) => {
            var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
            return 'R$ ' + value.toFixed(2);
          },
        }
      },
      plugins: {
        tooltips: {
          mode: 'index',
          intersect: false,

        },
        legend: {
          labels: {
            color: textColor
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder,
            drawBorder: false
          }
        },
        y: {
          stacked: true,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder,
            drawBorder: false
          }
        }
      }
    };

}
