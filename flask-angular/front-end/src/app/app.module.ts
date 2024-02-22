import { NgModule, DEFAULT_CURRENCY_CODE, LOCALE_ID } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';

import { NgChartsModule } from 'ng2-charts';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';



import { MainComponent } from './template/main/main.component';
import { NavComponent } from './template/nav/nav.component';
import { ContentComponent } from './template/content/content.component';
import { FooterComponent } from './template/footer/footer.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';





import { OperacoesModule } from './pages/operacoes/operacoes.module';
import { CarteirasModule } from './pages/carteiras/carteiras.module';
import { SharedModule } from './shared/shared.module';

import { DividendosComponent } from './pages/dividendos/dividendos.component';
import { AtivosModule } from './pages/ativos/ativos.module';
import { SetupsModule } from './pages/setups/setups.module';
 



registerLocaleData(localePt)

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    NavComponent,
    ContentComponent,
    FooterComponent,


    DashboardComponent,
    DividendosComponent,

  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,


    AppRoutingModule,
    SharedModule,


    OperacoesModule,
    CarteirasModule,
    AtivosModule,
    SetupsModule,

    NgChartsModule
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt-BR' },
    { provide: DEFAULT_CURRENCY_CODE, useValue: 'BRL' },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
