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

  constructor(private service: CarteiraService, private modalService: ModalService) {
    this.formNovaMovimentacao = new FormGroup({
      data_referencia: new FormControl(new Date()),
      descricao: new FormControl(),
      tipo: new FormControl(),
      valor: new FormControl(0.0),
      carteira_id: new FormControl(),
    });
  }


  ngOnInit(): void {    
    this.onLoad()
  }


  private onLoad() {
    this.service.load_movimentacoes().subscribe({
      next: (resp) => this.movimentacoes = resp.data,
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

  showFormNew() {
    if (this.carteiras.length == 0){
      this.service.loadAll().subscribe(resp => this.carteiras = resp.data)
    }
    
    this.modalService.open('modalNewMov')
  }


  hideFormMov() {
    this.modalService.close('modalNewMov')
  }
}



