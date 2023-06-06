import { Component } from '@angular/core';

import {FormGroup, FormControl, FormsModule, ReactiveFormsModule} from '@angular/forms';

import { OperacoesService } from 'src/app/services/operacoes.service';


@Component({
  selector: 'app-nao-encerradas',
  templateUrl: './nao-encerradas.component.html',
  styleUrls: ['./nao-encerradas.component.scss']
})
export class NaoEncerradasComponent {

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
   this.onLoad('')
  }

  onFilter():void {    
    console.log(this.formFiltrer.value)
    this.onLoad(this.formFiltrer.value.start)
  }
  
  onFilterData(encerramento:string){
    this.onLoad(encerramento)
  }

  private onLoad(start:string){
    this.service.load_opened(start).subscribe(resp => {   
      this.items = resp.data.items
      this.summary = resp.data.summary
    })
  }


}
