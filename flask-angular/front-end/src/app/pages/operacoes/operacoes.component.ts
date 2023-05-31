import { Component, OnInit } from '@angular/core';
import { OperacoesService } from 'src/app/services/operacoes.service';

@Component({
  selector: 'app-operacoes',
  templateUrl: './operacoes.component.html',
  styleUrls: ['./operacoes.component.scss']
})
export class OperacoesComponent implements OnInit {

  public items: any[];
  public summary: any;

  constructor(private service: OperacoesService) {
    this.items = []
  }

  ngOnInit(): void {
    this.service.load().subscribe(resp => {
      console.log(resp)
      this.items = resp.data.items
      this.summary = resp.data.summary
    })
  }


}
