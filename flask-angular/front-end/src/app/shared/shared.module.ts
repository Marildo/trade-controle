import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


import { NgChartsModule } from 'ng2-charts';

import { MaterialModule } from './material.module';
import { PrimeModule } from './prime.module';

import { ComponentsModule } from '../components/components.module';


@NgModule({
  declarations: [
   
  ],

  imports: [
    FormsModule,
    ReactiveFormsModule,

    NgChartsModule,

    MaterialModule,
    PrimeModule,
    ComponentsModule,




  ],
  exports: [
    FormsModule,
    ReactiveFormsModule,
    NgChartsModule,

    MaterialModule,
    PrimeModule,
    ComponentsModule,

  ]
})
export class SharedModule { }
