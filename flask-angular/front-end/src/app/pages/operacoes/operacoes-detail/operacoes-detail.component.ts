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
  public formFiltrer:FormGroup;

  constructor(private service: OperacoesService) {
    this.items = [];

    this.formFiltrer = new FormGroup({
      start: new FormControl(this.default_date),
      end: new FormControl(this.default_date),
    });
  }

  ngOnInit(): void {
   this.onLoad('','')
  }

  onFilter():void {    
    console.log(this.formFiltrer.value)
    this.onLoad(this.formFiltrer.value.start,'')
  }
  
  onFilterData(encerramento:string){
    this.onLoad(encerramento, '')
  }

  onFilterAtivo(ativo:string){
    this.onLoad('', ativo)
  }

  private onLoad(start:string, ativo:string){
    this.service.load_closed(start, ativo).subscribe(resp => {   
      this.items = resp.data.items
      this.summary = resp.data.summary
    })
  }



}
