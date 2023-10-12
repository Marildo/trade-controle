import { Component } from '@angular/core';
import { ChartType, ChartConfiguration } from 'chart.js';
import { ParValues } from '../../components/panel-result/par-value';
import { DividendosService } from './dividendos.service';




@Component({
  selector: 'app-dividendos',
  templateUrl: './dividendos.component.html',
  styleUrls: ['./dividendos.component.scss']
})

export class DividendosComponent {

  public results: ParValues[] = [];
  public lineChartType: ChartType = 'line';
  private lineChartLabels: string[] = [];
  private lineChartDataRows: number[] = [];

  constructor(private service: DividendosService) {
    this.loadAll()

  }

  private loadAll() {
    this.service.loadAll().subscribe(resp => {
      this.results = []
      this.results.push({ label: 'Mês', value: resp.data.month })
      this.results.push({ label: 'Ano', value: resp.data.year })
      this.results.push({ label: 'Total', value: resp.data.total })

      const group_month = resp.data.items.reduce((acc: any, item: any) => {
        const xdate = new Date(item.data_ref)
        const dtpgto = xdate.setMonth(xdate.getMonth() + 1)
        const key = new Date(dtpgto).toLocaleDateString()
        if (!acc[key]) {
          acc[key] = {
            total: 0
          };
        }

        acc[key].total += item.total
        return acc
      }, {}
      )

      //console.log(group_month)

      for (let propriedade in group_month) {
        let total = group_month[propriedade].total
        if (total != 0) {
          let split = propriedade.split('/')
          let label = `${split[1]}/${split[2]}`
          this.lineChartLabels.push(label)
          this.lineChartDataRows.push(total)
        }

      }

    })
  }



  public lineChartData(): ChartConfiguration['data'] {
    const data = {
      datasets: [
        {
          data: this.lineChartDataRows,
          label: 'Evolução de dividendos',
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

  OnFindNew() {
    this.service.findNew().subscribe(resp => {
      console.log(resp)
      this.loadAll()
    })
  }
}
