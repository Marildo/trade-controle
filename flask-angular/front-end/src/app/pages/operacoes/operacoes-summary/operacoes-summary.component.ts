import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import {  HttpParams } from '@angular/common/http';
import { OperacoesService } from 'src/app/services/operacoes.service';


@Component({
  selector: 'app-operacoes-summary',
  templateUrl: './operacoes-summary.component.html',
  styleUrls: ['./operacoes-summary.component.scss']
})
export class OperacoesSummaryComponent {
  private default_date = new Date(2020, 8, 10).toISOString().split('T')[0]


  
  public items: any[];
  public summary: any;
  public formFiltrer:FormGroup;

  private filter = new Map();

  constructor(private service: OperacoesService) {
    this.items = [];

    this.formFiltrer = new FormGroup({
      start: new FormControl(this.default_date),
      end: new FormControl(this.default_date),
    });

   
  }

  ngOnInit(): void {
   this.onLoad()
  }
  
  onFilterAtivo(ativo:string){
    this.filter.set('ativo_id',ativo)
    this.onLoad()
  }

  private onLoad(){
    this.service.load_summary(this.filter).subscribe(resp => {   
      this.items = resp.data.items
      this.summary = resp.data.summary
    })
  }


}