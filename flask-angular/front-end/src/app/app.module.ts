import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';


import {MatIconModule} from '@angular/material/icon';

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

@NgModule({
  declarations: [
   

    AppComponent,
    HomeComponent,
    MainComponent,
    NavComponent,
    ContentComponent,
    FooterComponent,
    OperacoesComponent,
    CarteirasComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,

    MatIconModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
