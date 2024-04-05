import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-ativos-ibovespa-item',
  templateUrl: './ativos-ibovespa-item.component.html',
  styleUrls: ['./ativos-ibovespa-item.component.scss']
})
export class AtivosIbovespaItemComponent implements OnInit {

  private ativo_id: number;

  constructor(private activatedRoute: ActivatedRoute) {
    this.ativo_id = 0
  }

  ngOnInit(): void {
    this.ativo_id = parseInt(this.activatedRoute.snapshot.params['id']);
    console.log(this.ativo_id)
  }
}
