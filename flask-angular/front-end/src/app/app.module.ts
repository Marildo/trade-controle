import { NgModule, DEFAULT_CURRENCY_CODE, LOCALE_ID } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';



import { MatNativeDateModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MainComponent } from './template/main/main.component';
import { NavComponent } from './template/nav/nav.component';
import { ContentComponent } from './template/content/content.component';
import { FooterComponent } from './template/footer/footer.component';
import { OperacoesComponent } from './pages/operacoes/operacoes.component';
import { CarteirasComponent } from './pages/carteiras/carteiras.component';


import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';
import { TabHeaderComponent } from './components/tab/tab-header/tab-header.component';
import { TabItemComponent } from './components/tab/tab-item/tab-item.component';
import { TabBodyComponent } from './components/tab/tab-body/tab-body.component';
import { TabComponent } from './components/tab/tab/tab.component';
import { NaoEncerradasComponent } from './pages/operacoes/nao-encerradas/nao-encerradas.component';
registerLocaleData(localePt)

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MainComponent,
    NavComponent,
    ContentComponent,
    FooterComponent,
    OperacoesComponent,
    CarteirasComponent,
    TabHeaderComponent,
    TabItemComponent,
    TabBodyComponent,
    TabComponent,
    NaoEncerradasComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,

    MatNativeDateModule,
    MatIconModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatButtonModule
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt-BR' },
    { provide: DEFAULT_CURRENCY_CODE, useValue: 'BRL' },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
