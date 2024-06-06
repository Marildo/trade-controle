import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ModalService } from 'src/app/components/modal/modal-service';


import { OperacoesService } from 'src/app/pages/operacoes/operacoes.service';
import { CarteiraService } from '../../carteiras/carteira.service';
import { SetupService } from 'src/app/service/api/setup.service';
import { AtivoService } from 'src/app/service/api/ativo.service';

@Component({
  selector: 'app-operacoes-detail',
  templateUrl: './operacoes-detail.component.html',
  styleUrls: ['./operacoes-detail.component.scss']
})
export class OperacoesDetailComponent {

  public items: any[];
  public carteiras: any[];
  public setups: any[];
  public ativos: any[];

  public summary: any;
  public formFiltrer: FormGroup;
  public formOperacao: FormGroup;
  public hiddenFilter: boolean;
  private modalEdit = "modalEdit"

  private filter = new Map();

  constructor(private route: ActivatedRoute,
    private service: OperacoesService,
    private carteiraService: CarteiraService,
    private setupService: SetupService,
    private ativoService: AtivoService,

    private messageService: MessageService, private modalService: ModalService) {
    this.items = [];
    this.carteiras = [];
    this.setups = [];
    this.ativos = [];
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
      daytrade: new FormControl(true),
      nota: new FormControl(),
      codigo: new FormControl(),
      carteira_id: new FormControl(),
      tipo_investimento: new FormControl(),
    });

    this.formOperacao = new FormGroup({
      ativo: new FormControl(),
      ativo_id: new FormControl(),
      carteira: new FormControl(),
      carteira_id: new FormControl(),
      compra_hist_id: new FormControl(),
      compra_venda: new FormControl(),
      custos: new FormControl(),
      data_compra: new FormControl(),
      data_encerramento: new FormControl(),
      data_venda: new FormControl(),
      daytrade: new FormControl(),
      encerrada: new FormControl(),
      id: new FormControl(),
      irpf: new FormControl(),
      nota_compra: new FormControl(),
      nota_compra_id: new FormControl(),
      nota_venda: new FormControl(),
      nota_venda_id: new FormControl(),
      pm_compra: new FormControl(),
      pm_venda: new FormControl(),
      qtd_compra: new FormControl(),
      qtd_venda: new FormControl(),
      resultado: new FormControl(),
      venda_hist_id: new FormControl(),
      setup: new FormControl(),
      setup_id: new FormControl(),
      payoff: new FormControl(0),
      tendencia: new FormControl(),
      quality: new FormControl(),
      segui_plano: new FormControl(true),
      contexto: new FormControl(true),
      obs: new FormControl("")
    });

    this.formOperacao.get('tendencia')?.valueChanges.subscribe(v => this.onCalculeQuality())
    this.formOperacao.get('payoff')?.valueChanges.subscribe(v => this.onCalculeQuality())
    this.formOperacao.get('segui_plano')?.valueChanges.subscribe(v => this.onCalculeQuality())
    this.formOperacao.get('contexto')?.valueChanges.subscribe(v => this.onCalculeQuality())
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

  onEditar(id: string): void {
    if (this.carteiras.length == 0) {
      this.carteiraService.loadAll().subscribe(resp => {
        this.carteiras = resp.data
        this.ativoService.loadAll().subscribe(resp => {
          this.ativos = resp.data
          this.setupService.loadAll().subscribe(resp => this.setups = resp.data)
        })
      })
    }



    const item = this.items.filter(f => f.id == id)[0]

    this.formOperacao.setValue(item)
    this.modalService.open(this.modalEdit)
  }

  hideFormOperacao(): void {
    this.modalService.close(this.modalEdit)
  }

  saveOperacao(): void {
    this.service.update(this.formOperacao.value).subscribe({
      next: value => {
        this.modalService.close(this.modalEdit)
        this.onLoad()

      },
      error(err) {
        console.log(err)
      },
    })

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

  private onCalculeQuality(): void {
    let quality = 0
    const tendencia = this.formOperacao.get('tendencia')?.value
    const payoff = this.formOperacao.get('payoff')?.value
    const segui_plano = this.formOperacao.get('segui_plano')?.value
    const contexto = this.formOperacao.get('contexto')?.value


    if (tendencia === 'FAVOR') {
      quality += 30
    }
    else if (tendencia === 'LATERAL') {
      quality += 10
    }
    else {
      quality += 0
    }

    quality += payoff * 5
    quality += segui_plano ? 25 : 0
    quality += contexto ? 25 : 0

    quality = quality / 10
    if (quality > 10) {
      quality = 10
    } else {
      if (quality < 0)
        quality = 0
    }


    this.formOperacao.get('quality')?.setValue(quality);

  }
}


// TODO  - Visualizar arquivo pdf