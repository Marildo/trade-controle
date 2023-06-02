import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl, FormsModule, ReactiveFormsModule} from '@angular/forms';

import { OperacoesService } from 'src/app/services/operacoes.service';

@Component({
  selector: 'app-operacoes',
  templateUrl: './operacoes.component.html',
  styleUrls: ['./operacoes.component.scss']
})
export class OperacoesComponent implements OnInit {

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

  private onLoad(start:string){
    this.service.load(start).subscribe(resp => {   
      this.items = resp.data.items
      this.summary = resp.data.summary
    })
  }

}
