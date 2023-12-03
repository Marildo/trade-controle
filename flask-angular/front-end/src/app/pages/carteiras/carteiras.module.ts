import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CarteiraRoutingModule } from './carteiras.routing.module';
import { CarteiraMainComponent } from './carteira-main/carteira-main.component';
import { CarteiraMovimentacoesComponent } from './carteira-movimentacoes/carteira-movimentacoes.component';
import { CarteiraHistoricoComponent } from './carteira-historico/carteira-historico.component';
import { CarteirasComponent } from './carteira/carteiras.component';
import { SharedModule } from 'src/app/shared/shared.module';

 


@NgModule({
  declarations: [
    CarteirasComponent,
    CarteiraMainComponent,
    CarteiraHistoricoComponent,
    CarteiraMovimentacoesComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    CarteiraRoutingModule,

  ]
})
export class CarteirasModule { }
