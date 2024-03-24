import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ModalService } from 'src/app/components/modal/modal-service';
import { CarteiraService } from '../carteira.service';

@Component({
  selector: 'app-carteira-movimentacoes',
  templateUrl: './carteira-movimentacoes.component.html',
  styleUrls: ['./carteira-movimentacoes.component.scss']
})
export class CarteiraMovimentacoesComponent implements OnInit {


  public movimentacoes: any[] = []
  public carteiras: any[] = []
  public formNovaMovimentacao: FormGroup;
  public start_date!: any;
  public end_date!: any;
  public total = 0;

  constructor(private service: CarteiraService, private modalService: ModalService) {
    this.formNovaMovimentacao = new FormGroup({
      data_referencia: new FormControl(new Date()),
      descricao: new FormControl(),
      tipo: new FormControl(),
      valor: new FormControl(0.0),
      carteira_id: new FormControl(),
    });


    const today = new Date()
    this.start_date = new Date(today.setDate(0)).toISOString().split('T')[0];
    this.end_date = new Date().toISOString().split('T')[0];
  }


  ngOnInit(): void {
    this.onLoad()
  }


  onLoad() {
    const filter = new Map();
    filter.set('start_date', this.start_date)
    filter.set('end_date', this.end_date)
    this.service.load_movimentacoes(filter).subscribe({
      next: (resp) => {
        this.movimentacoes = resp.data;
        this.total = this.movimentacoes.reduce((soma, item) => soma + item.valor, 0)
      },
      error: (e) => console.error(e),
    })
  }


  saveMovimentacao() {
    this.service.saveMovimentacao(this.formNovaMovimentacao.value).subscribe({
      complete: () => {
        this.formNovaMovimentacao.reset()
        this.onLoad()
      },
      error: console.error
    })
  }


  delete_movimentacao(id: number) {
    this.service.delete_movimentacao(id).subscribe({
      complete: () => this.onLoad(),
      error: console.error
    })
  }

  showFormNew() {
    if (this.carteiras.length == 0) {
      this.service.loadAll().subscribe(resp => this.carteiras = resp.data)
    }

    this.modalService.open('modalNewMov')
  }


  hideFormMov() {
    this.modalService.close('modalNewMov')
  }
}



