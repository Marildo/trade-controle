import { Component, OnInit, EventEmitter } from '@angular/core';
import { OperacoesService } from '../services/operacoes.service';

@Component({
  selector: 'app-operacoes-dashboard',
  templateUrl: './operacoes-dashboard.component.html',
  styleUrls: ['./operacoes-dashboard.component.scss']
})
export class OperacoesDashboardComponent implements OnInit {

  public onLoad = new EventEmitter()
  constructor(private service: OperacoesService) { }

  ngOnInit() {
    this.service.load_dashboard().subscribe({
      next: (resp) => {
        this.onLoad.emit(resp)
      },
      error: (e) => {
        console.error(e);
      },
    })
  }
}
