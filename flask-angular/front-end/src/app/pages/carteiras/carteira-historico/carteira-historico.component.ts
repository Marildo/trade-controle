import { Component, OnInit } from '@angular/core';
import { CarteiraService } from '../carteira.service';

@Component({
  selector: 'app-carteira-historico',
  templateUrl: './carteira-historico.component.html',
  styleUrls: ['./carteira-historico.component.scss']
})
export class CarteiraHistoricoComponent implements OnInit {


  public historicos: any[] = []
 

  constructor(private service: CarteiraService) {
 
  }

  
  ngOnInit(): void {    
    this.onLoad()
  }


  private onLoad() {
    this.service.load_historicos().subscribe({
      next: (resp) => this.historicos = resp.data,
      error: (e) => console.error(e),
    })
  }

}
