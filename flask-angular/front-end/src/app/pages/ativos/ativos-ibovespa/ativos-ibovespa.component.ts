import { Component, OnInit } from '@angular/core';
import { AtivoService } from 'src/app/service/api/ativo.service';

@Component({
  selector: 'app-ativos-ibovespa',
  templateUrl: './ativos-ibovespa.component.html',
  styleUrls: ['./ativos-ibovespa.component.scss']
})
export class AtivosIbovespaComponent implements OnInit{

  public ativos: any[];

  constructor ( private ativoService: AtivoService) {
    this.ativos = []
  }
  ngOnInit(): void {
     this.load()
  }
  
  load(){

    this.ativoService.loadAll().subscribe({
      next: (resp) => {
        this.ativos = resp.data
      }
    })
  }
}
