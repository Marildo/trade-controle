import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

 
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { DividendosComponent } from './pages/dividendos/dividendos.component';
import { CarteiraMainComponent } from './pages/carteiras/carteira-main/carteira-main.component';


 
const routes: Routes = [
  {path:'', component:DashboardComponent, pathMatch: 'full'},
  {path:'carteiras', component:CarteiraMainComponent},
  {path: 'dividendos', component:DividendosComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
