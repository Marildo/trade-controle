
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';




import { CarteiraMainComponent } from './carteira-main/carteira-main.component';
import { CarteirasComponent } from './carteira/carteiras.component';
import { CarteiraMovimentacoesComponent } from './carteira-movimentacoes/carteira-movimentacoes.component';



const CarteiraRouters: Routes = [
  {
    path: 'carteiras',
    component: CarteiraMainComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: CarteirasComponent },
      { path: 'movimentacoes', component: CarteiraMovimentacoesComponent },
     
    ]
  }
]


@NgModule({
  imports: [RouterModule.forChild(CarteiraRouters)],
  exports: [RouterModule]
})
export class CarteiraRoutingModule { }






