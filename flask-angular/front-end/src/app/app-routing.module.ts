import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

 
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { DividendosComponent } from './pages/dividendos/dividendos.component';


 
const routes: Routes = [
  {path:'dashboard', component:DashboardComponent, pathMatch: 'full'},
  {path: 'dividendos', component:DividendosComponent},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
