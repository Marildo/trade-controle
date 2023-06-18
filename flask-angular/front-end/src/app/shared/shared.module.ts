import { NgModule } from '@angular/core';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { ChartModule } from 'primeng/chart';
import { NgChartsModule } from 'ng2-charts';

import { MaterialModule } from './material.module';
import { ComponentsModule } from '../components/components.module';








@NgModule({
  declarations: [
   
  ],

  imports: [
    FormsModule,
    ReactiveFormsModule,
    ChartModule,
    NgChartsModule,

    MaterialModule,
    ComponentsModule,




  ],
  exports: [
    FormsModule,
    ReactiveFormsModule,
    ChartModule,
    NgChartsModule,
    MaterialModule,
    ComponentsModule,

  ]
})
export class SharedModule { }
