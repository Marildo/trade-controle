import { NgModule } from '@angular/core';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { ChartModule } from 'primeng/chart';
import { NgChartsModule } from 'ng2-charts';

import { MaterialModule } from './material.module';


@NgModule({
  imports: [
    FormsModule,
    ReactiveFormsModule,
    ChartModule,
    NgChartsModule,
    MaterialModule],
  exports: [
    FormsModule,
    ReactiveFormsModule,
    ChartModule,
    NgChartsModule,
    MaterialModule
  ]
})
export class SharedModule { }
