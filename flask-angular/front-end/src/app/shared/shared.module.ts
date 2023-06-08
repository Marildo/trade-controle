import { NgModule } from '@angular/core';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';


 
import { MaterialModule } from './material.module';


@NgModule({
  imports: [
    FormsModule,
    
    ReactiveFormsModule,
    MaterialModule
  ],
  exports: [
    FormsModule,
    ReactiveFormsModule,

    MaterialModule
  ]
})
export class SharedModule { }
