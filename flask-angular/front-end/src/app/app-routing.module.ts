import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

 
import { CarteirasComponent } from './pages/carteiras/carteiras.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { DividendosComponent } from './pages/dividendos/dividendos.component';


 
const routes: Routes = [
  {path:'', component:DashboardComponent, pathMatch: 'full'},
  {path:'carteiras', component:CarteirasComponent},
  {path: 'dividendos', component:DividendosComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
