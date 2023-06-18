import { NgModule, DEFAULT_CURRENCY_CODE, LOCALE_ID } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';



import { MainComponent } from './template/main/main.component';
import { NavComponent } from './template/nav/nav.component';
import { ContentComponent } from './template/content/content.component';
import { FooterComponent } from './template/footer/footer.component';
import { CarteirasComponent } from './pages/carteiras/carteiras.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';


import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';


import { OperacoesModule } from './pages/operacoes/operacoes.module';
import { SharedModule } from './shared/shared.module';
import { NgChartsModule } from 'ng2-charts';



registerLocaleData(localePt)

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    NavComponent,
    ContentComponent,
    FooterComponent,

    
    CarteirasComponent,
  
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,


    SharedModule,



    AppRoutingModule,

    OperacoesModule,
     NgChartsModule
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt-BR' },
    { provide: DEFAULT_CURRENCY_CODE, useValue: 'BRL' },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
