import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';


import { OperacoesService } from 'src/app/pages/operacoes/services/operacoes.service';

@Component({
  selector: 'app-operacoes-detail',
  templateUrl: './operacoes-detail.component.html',
  styleUrls: ['./operacoes-detail.component.scss']
})
export class OperacoesDetailComponent {

  public items: any[];
  public summary: any;
  public formFiltrer: FormGroup;
  public hiddenFilter: boolean;

  private filter = new Map();

  constructor(private route: ActivatedRoute, private service: OperacoesService, private messageService: MessageService) {
    this.items = [];
    this.hiddenFilter = true;
    this.summary = { 'numero_operacoes': 0 }

    const today = new Date();
    const default_date = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0]

    this.formFiltrer = new FormGroup({
      start_encerramento: new FormControl(default_date),
      end_encerramento: new FormControl(),
      start_data_compra: new FormControl(),
      end_data_compra: new FormControl(),
      start_data_venda: new FormControl(),
      end_data_venda: new FormControl(),
      encerrada: new FormControl(true),
      daytrade: new FormControl(false),
      nota: new FormControl(),
      codigo: new FormControl(),
      carteira_id: new FormControl(),
      tipo_investimento: new FormControl(),
    });
  }

  ngOnInit(): void {
    const params = this.route.snapshot.queryParams;
    if ('file_id' in params) {
      this.filter.set('file_id', params['file_id'])
      this.onLoad()
    } else {
      this.onFilter()
    }

  }

  onFilter(): void {
    this.filter.clear()
    const form = this.formFiltrer.value
    Object.keys(form).forEach((prop) => {
      if (form[prop] != null) {
        this.filter.set(prop, form[prop])
      }
    })
    this.onLoad()
  }

  onHiddeFilter(): void {
    this.hiddenFilter = true;
  }

  clearFilter(): void {
    this.filter.clear()
    this.formFiltrer.reset()
    this.onLoad()
    this.onHiddeFilter()
  }

  onFilterDataCompra(data: string): void {
    this.filter.clear()
    this.filter.set('start_data_compra', data)
    this.filter.set('end_data_compra', data)
    this.onLoad()
  }

  onFilterDataVenda(data: string): void {
    this.filter.clear()
    this.filter.set('start_data_venda', data)
    this.filter.set('end_data_venda', data)
    this.onLoad()
  }


  onFilterAtivo(ativo: string): void {
    this.filter.set('ativo_id', ativo)
    this.onLoad()
  }

  onFilterNotaCompra(nota: string): void {
    this.filter.clear()
    this.filter.set('nota_compra', nota)
    this.onLoad()
  }

  onFilterNotaVenda(nota: string): void {
    this.filter.clear()
    this.filter.set('nota_venda', nota)
    this.onLoad()
  }

  private onLoad(): void {
    this.service.load_detail(this.filter)
      .subscribe({
        next: (resp) => {
          this.items = resp.data.items
          this.summary = resp.data.summary
          this.onHiddeFilter()
        },
        error: (e) => {
          console.error(e)
        }
      })
  }


}


// TODO  - Visualizar arquivo pdf