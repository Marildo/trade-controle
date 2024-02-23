
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SetupMainComponent } from './setup-main/setup-main.component';
import { SetupDashboardComponent } from './setup-dashboard/setup-dashboard.component';
import { SetupScreeningComponent } from './setup-screening/setup-screening.component';
import { SetupBacktestComponent } from './setup-backtest/setup-backtest.component';



const setupsRouters: Routes = [
    {
        path: 'setups',
        component: SetupMainComponent,
        children: [
            { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
            { path: 'dashboard', component: SetupDashboardComponent },
            { path: 'screening', component: SetupScreeningComponent },
            { path: 'backtest', component: SetupBacktestComponent },
        ]
    }
]


@NgModule({
    imports: [RouterModule.forChild(setupsRouters)],
    exports: [RouterModule]
})
export class SetupRoutingModule { }



