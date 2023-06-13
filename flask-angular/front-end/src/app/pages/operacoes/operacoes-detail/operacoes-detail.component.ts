import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { OperacoesService } from 'src/app/services/operacoes.service';

@Component({
  selector: 'app-operacoes-detail',
  templateUrl: './operacoes-detail.component.html',
  styleUrls: ['./operacoes-detail.component.scss']
})
export class OperacoesDetailComponent {

  private default_date = new Date(2020, 8, 10).toISOString().split('T')[0]


  public items: any[];
  public summary: any;
  public formFiltrer: FormGroup;
  public hiddenFilter: boolean;

  private filter = new Map();

  constructor(private service: OperacoesService) {
    this.items = [];
    this.hiddenFilter = true;
    this.summary = { 'numero_operacoes': 0 }

    this.formFiltrer = new FormGroup({
      start: new FormControl(this.default_date),
      end: new FormControl(this.default_date),
    });
  }

  ngOnInit(): void {
    this.onLoad()
  }

  onFilter(): void {
    this.onLoad()
  }

  onShowFilter(): void {
    this.hiddenFilter = false;
  }

  onHiddeFilter(): void {
    console.log('fechando')
    this.hiddenFilter = true;
  }

  clearFilter(): void {
    this.filter.clear()
    this.onLoad()
    this.onHiddeFilter()
  }

  onFilterDataCompra(data: string): void {
    this.filter.set('data_compra', data)
    this.onLoad()
  }

  onFilterDataVenda(data: string): void {
    this.filter.set('data_venda', data)
    this.onLoad()
  }


  onFilterAtivo(ativo: string): void {
    this.filter.set('ativo_id', ativo)
    this.onLoad()
  }

  onFilterNotaCompra(nota: string): void {
    this.filter.set('nota_compra', nota)
    this.onLoad()
  }

  onFilterNotaVenda(nota: string): void {
    this.filter.set('nota_venda', nota)
    this.onLoad()
  }

  private onLoad(): void {
    this.hiddenFilter = false;

    this.service.load_closed(this.filter)
      .subscribe({
        next: (resp) => {
          this.items = resp.data.items
          this.summary = resp.data.summary
        },
        error: (e) => {
          console.error(e)
        }
      })
  }


}
