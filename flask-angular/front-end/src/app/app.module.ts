import { NgModule, DEFAULT_CURRENCY_CODE, LOCALE_ID } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';





import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


import { MainComponent } from './template/main/main.component';
import { NavComponent } from './template/nav/nav.component';
import { ContentComponent } from './template/content/content.component';
import { FooterComponent } from './template/footer/footer.component';
import { CarteirasComponent } from './pages/carteiras/carteiras.component';


import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';
import { TabHeaderComponent } from './components/tab/tab-header/tab-header.component';
import { TabItemComponent } from './components/tab/tab-item/tab-item.component';
import { TabBodyComponent } from './components/tab/tab-body/tab-body.component';
import { TabComponent } from './components/tab/tab/tab.component';

import { OperacoesModule } from './pages/operacoes/operacoes.module';
import { SharedModule } from './shared/shared.module';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
registerLocaleData(localePt)

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    NavComponent,
    ContentComponent,
    FooterComponent,

    
    CarteirasComponent,
    TabHeaderComponent,
    TabItemComponent,
    TabBodyComponent,
    TabComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,


    SharedModule,



    AppRoutingModule,

    OperacoesModule
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt-BR' },
    { provide: DEFAULT_CURRENCY_CODE, useValue: 'BRL' },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
