import { Component, OnInit } from '@angular/core';
import { CarteiraService } from '../carteira.service';
import { ModalService } from 'src/app/components/modal/modal-service';
import { FormControl, FormGroup } from '@angular/forms';


@Component({
  selector: 'app-carteiras',
  templateUrl: './carteiras.component.html',
  styleUrls: ['./carteiras.component.scss']
})
export class CarteirasComponent implements OnInit {



  public summarized = {
    resultado: 0,
    saldo_ativos: 0,
    saldo_caixa: 0,
    total: 0
  }

  public carteiras: any[] = []
  public formCarteira: FormGroup;

  constructor(private service: CarteiraService, private modalService: ModalService) {
    this.formCarteira = new FormGroup({
      nome: new FormControl(),
      descricao: new FormControl(),
      tipo: new FormControl(),
      daytrade: new FormControl(false),
      dividendos: new FormControl(false),
      buyhold: new FormControl(false),
    });
  }



  ngOnInit(): void {
    this.loadCarteiras()

  }

  loadCarteiras(): void {
    this.service.loadAll().subscribe(resp => {
      this.carteiras = resp.data

      for (const item of this.carteiras) {
        this.summarized.resultado += item.resultado
        this.summarized.saldo_ativos += item.saldo_ativos
        this.summarized.saldo_caixa += item.saldo_caixa
        this.summarized.total += item.saldo_caixa + item.saldo_ativos
      }
    })
  }

  showFormCarteira(): void {
    this.modalService.open('modalCarteira')
  }

  hideFormCarteira(): void {
    this.modalService.close('modalCarteira')
  }

  saveCarteira(): void {
    this.service.save(this.formCarteira.value).subscribe({
      next: (resp) => {
        this.loadCarteiras()
        this.hideFormCarteira
      },
      error: (e) => {
        console.error(e)
      }
    })
  }
}

